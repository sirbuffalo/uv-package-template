Delete this if not using continous deployment to another machine via a github action

------------

High-level requirements from the deploy job:
- A service user (vantracker) owns the app dir /opt/vantracker/vantracker and runs the systemd unit.
- The deploy user (DEPLOY_USER) can SSH in and run:
  - rsync as the service user without a password
  - uv sync as the service user without a password
  - systemctl restart vantracker without a password
- uv is installed for the service user (vantracker) and Python 3.13 is available.
- Server has an environment file with secrets loaded by systemd.


See commented out job in .github/ci-deploy.yml
env:
  # Configuration for deployment task
  SERVICE_USER: "uv-package-template"
  SERVICE_NAME: "uv-package-template"
  APP_USER_ROOT: "/opt/${{ env.SERVICE_USER }}"
  APP_DIR: "${{ env.SERVICE_USER }}/${{ env.SERVICE_NAME }}"
  CONCURRENCY_GROUP: "${{ env.SERVICE_NAME }}-prod"


1) Create users, dirs, packages
- Create service user with no interactive shell and a HOME under /opt/vantracker.
- Create deploy user with SSH login.
- Install minimal packages.

````bash
# Create service user (no interactive shell)
sudo useradd --system --create-home --home /opt/vantracker --shell /usr/sbin/nologin vantracker

# Create app dir and assign ownership
sudo mkdir -p /opt/vantracker/vantracker
sudo chown -R vantracker:vantracker /opt/vantracker

# Create deploy user (interactive)
sudo adduser deployer
# Or: sudo useradd -m -s /bin/bash deployer && sudo passwd deployer

# Base packages
sudo apt update
sudo apt install -y rsync openssh-server curl
````

2) Install uv for the service user and pin Python
The workflow runs dependency install as the service user via sudo -u vantracker -H … uv sync --frozen. Install uv into the service user’s HOME and set a default Python 3.13.

````bash
sudo -u vantracker -H bash -lc '
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  uv --version
  uv python install --default 3.13
'
````

3) Systemd unit to run the app
- Loads secrets from an environment file.
- Ensures PATH includes uv.
- Points WorkingDirectory to /opt/vantracker/vantracker.
- Uses gunicorn bound to 127.0.0.1:9000 per README.md.

````ini
[Unit]
Description=VanTracker (Flask/Gunicorn)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=vantracker
Group=vantracker
WorkingDirectory=/opt/vantracker/vantracker
EnvironmentFile=/etc/vantracker.env
# Ensure uv is found; systemd does not inherit interactive PATHs
Environment=PATH=/opt/vantracker/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
# If you run without installing the package, ensure PYTHONPATH points at src
# Environment=PYTHONPATH=/opt/vantracker/vantracker/src

ExecStart=/opt/vantracker/.local/bin/uv run gunicorn -w 2 -b 127.0.0.1:9000 "vantracker.webhook:app"
Restart=on-failure
RestartSec=3s
KillSignal=SIGINT
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
````

4) Environment file with secrets
Matches what the app expects in get_drive_time.py, get_location.py, and webhook.py.

````bash
# Create env file (root-owned, 0600)
sudo install -m 0600 -o root -g root /dev/stdin /etc/vantracker.env <<'EOF'
GOOGLE_MAPS_API_KEY=...
TRACCAR_TOKEN=...
WEBHOOKS_BEARER_TOKEN=...
# If running without installing the package:
# PYTHONPATH=/opt/vantracker/vantracker/src
EOF
````

5) Sudoers for deploy workflow
The job in ci-deploy.yml runs:
- rsync with --rsync-path="sudo -n -u vantracker -H /usr/bin/rsync"
- remote install via sudo -n -u vantracker -H bash -lc '... uv sync --frozen'
- service restart via sudo -n systemctl restart vantracker

Grant only these specific commands NOPASSWD.

````conf
# Allow deployer to run specific commands without a password
Defaults:deployer !requiretty
deployer ALL=(vantracker) NOPASSWD: /usr/bin/rsync, /usr/bin/bash, /opt/vantracker/.local/bin/uv
deployer ALL=NOPASSWD: /bin/systemctl restart vantracker, /bin/systemctl status vantracker
````

6) SSH for deploy user
- Generate a deploy keypair off-box.
- Put the private key into the GitHub Actions secret DEPLOY_SSH_KEY.
- Put the corresponding public key into /home/deployer/.ssh/authorized_keys.

````bash
sudo -u deployer -H mkdir -p /home/deployer/.ssh
sudo -u deployer -H chmod 700 /home/deployer/.ssh
sudo -u deployer -H tee -a /home/deployer/.ssh/authorized_keys >/dev/null <<'EOF'
ssh-ed25519 AAAA... your-ci-public-key
EOF
sudo -u deployer -H chmod 600 /home/deployer/.ssh/authorized_keys
````

7) First-time enable and verify
- Seed the directory (optional) or let CI push the first time.
- Enable and start the service.

````bash
# Let CI populate /opt/vantracker/vantracker via rsync
sudo systemctl daemon-reload
sudo systemctl enable --now vantracker
sudo systemctl status vantracker --no-pager
tail -n 200 -f /opt/vantracker/vantracker/app.log
````

8) Networking notes
- The app binds to 127.0.0.1:9000 via gunicorn, so no public firewall opening is required.
- Ensure Traccar (on the same host) forwards to http://127.0.0.1:9000/traccar/events with the correct bearer per traccar.xml.

9) CI secrets
- In repo settings, set:
  - DEPLOY_HOST, DEPLOY_USER (e.g., deployer), DEPLOY_SSH_KEY (private key matching the authorized_keys above).

Optional hardening
- Restrict SSH: Disable root login; limit AllowUsers to deployer.
- Validate sudoers with visudo -c.
- Keep uv and Python fresh under the service user:
  sudo -u vantracker -H bash -lc 'uv self update && uv python install --default 3.13 && uv sync --frozen'

This setup aligns with your deploy job and runtime entrypoint. After CI pushes a change to main/master, the workflow rsyncs the repo, runs uv sync as the service user, and restarts the systemd unit.
"""uv-package-template package.

Lightweight public API surface and version metadata.
Avoid importing modules that perform network/auth at import time.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

# Expose package version without importing submodules with side effects.
try:  # pragma: no cover - trivial
    __version__ = version('uv_package_template')
except PackageNotFoundError:  # local editable or direct source usage
    __version__ = '0'

# Safe re-exports (no network or env side effects on import)

__all__ = [
    '__version__',
]

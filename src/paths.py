from __future__ import annotations

import os
import sys
from pathlib import Path


def app_root() -> Path:
    """Directory that contains config/, logs/, etc.

    - Frozen (PyInstaller): folder containing the executable
    - Dev: repository root (parent of src/)
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def resolve_path(p: str | Path) -> Path:
    path = Path(p)
    if path.is_absolute():
        return path
    return app_root() / path


def config_path(default: str = "config/config.yaml") -> Path:
    """Prefer config next to the app; fall back to CWD for convenience."""
    candidate = resolve_path(default)
    if candidate.exists():
        return candidate
    cwd_candidate = Path.cwd() / default
    if cwd_candidate.exists():
        return cwd_candidate
    return candidate

from __future__ import annotations

import os
from pathlib import Path


APP_NAME = "NerdScroll"


def app_data_dir() -> Path:
    """Return a writable per-user app data folder."""
    try:
        base = os.environ.get("LOCALAPPDATA")
        if base:
            path = Path(base) / APP_NAME
        else:
            path = Path.home() / f".{APP_NAME.lower()}"

        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception:
        fallback = Path.cwd() / "_nerd_scroll_runtime"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


def current_source_path() -> Path:
    """Return the GUI-to-runner handoff text file path."""
    return app_data_dir() / "current_source.txt"

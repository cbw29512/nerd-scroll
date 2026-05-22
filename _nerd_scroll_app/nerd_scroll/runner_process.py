from __future__ import annotations

import logging
import sys
from pathlib import Path


logger = logging.getLogger("nerd_scroll.runner_process")


def is_frozen_app() -> bool:
    """Return true when running from a PyInstaller-built executable."""
    return bool(getattr(sys, "frozen", False))


def resolve_app_root(root_arg: str | None, launcher_file: str) -> Path:
    """Resolve the folder that contains bundled packs and app files."""
    try:
        if root_arg:
            return Path(root_arg).resolve()
        if is_frozen_app():
            return Path(sys.executable).resolve().parent
        return Path(launcher_file).resolve().parents[1]
    except Exception:
        logger.exception("failed to resolve app root")
        raise


def build_runner_command(app_root: Path, source_path: Path, speed: str) -> list[str]:
    """Build the command that opens the terminal runner window."""
    try:
        if is_frozen_app():
            runner = app_root / "NerdScrollRunner.exe"
            if not runner.exists():
                raise FileNotFoundError(f"Runner executable not found: {runner}")
            return ["cmd.exe", "/k", str(runner), "--source", str(source_path), "--speed", speed]

        runner = app_root / "_nerd_scroll_app" / "runner_cli.py"
        if not runner.exists():
            raise FileNotFoundError(f"Runner script not found: {runner}")
        return ["cmd.exe", "/k", sys.executable, str(runner), "--source", str(source_path), "--speed", speed]
    except Exception:
        logger.exception("failed to build runner command")
        raise

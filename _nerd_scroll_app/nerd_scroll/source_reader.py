from __future__ import annotations

import logging
from pathlib import Path

from nerd_scroll.config import SourceSettings


logger = logging.getLogger("nerd_scroll.source_reader")


def load_source_lines(path: Path, settings: SourceSettings) -> list[str]:
    """Read the selected file as text; never execute it."""
    try:
        if path.suffix.lower() not in {ext.lower() for ext in settings.allowed_extensions}:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

        if settings.skip_empty_lines:
            lines = [line for line in lines if line.strip()]

        if not lines:
            raise ValueError(f"Selected file is empty: {path}")

        return lines
    except Exception:
        logger.exception("failed to load source file")
        raise

from __future__ import annotations

import logging
from pathlib import Path

from nerd_scroll.config import Settings


logger = logging.getLogger("nerd_scroll.drop_zone")


def find_drop_zone_source(root: Path, settings: Settings) -> Path:
    """Pick the newest supported user file from the stage-one folder."""
    try:
        folder = root / settings.drop_zone.folder_path
        folder.mkdir(parents=True, exist_ok=True)

        files = list_supported_files(
            folder=folder,
            allowed_extensions=settings.source.allowed_extensions,
            recursive=settings.drop_zone.recursive,
        )

        if not files:
            raise FileNotFoundError(
                "No supported file found in 1_DROP_TEXT_FILE_HERE. "
                "Drop a .txt, .log, .md, or code file there and run again."
            )

        return max(files, key=lambda path: path.stat().st_mtime)
    except Exception:
        logger.exception("failed to find drop-zone source")
        raise


def list_supported_files(
    folder: Path,
    allowed_extensions: list[str],
    recursive: bool,
) -> list[Path]:
    """Return local readable text-like files; never execute them."""
    try:
        pattern = "**/*" if recursive else "*"
        allowed = {ext.lower() for ext in allowed_extensions}
        ignored_names = {"README_DROP_FILES_HERE.txt"}

        results = []
        for path in folder.glob(pattern):
            if path.is_file() and path.name not in ignored_names:
                if path.suffix.lower() in allowed:
                    results.append(path)

        return results
    except Exception:
        logger.exception("failed to list drop-zone files")
        raise

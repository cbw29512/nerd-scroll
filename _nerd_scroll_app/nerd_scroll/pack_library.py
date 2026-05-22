from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path

from nerd_scroll.app_paths import app_data_dir


logger = logging.getLogger("nerd_scroll.pack_library")
ALLOWED_PACK_EXTENSIONS = {".txt", ".log", ".md", ".nscroll"}
DROP_FOLDER_NAME = "3_DROP_PACKS_HERE"
BUNDLED_PACK_FOLDER_NAME = "bundled_packs"


@dataclass(frozen=True)
class PackItem:
    """Saved Nerd Scroll pack file."""

    title: str
    path: Path
    recommended_speed: str = "normal"


def pack_library_dir() -> Path:
    """Return the saved user pack library folder."""
    path = app_data_dir() / "packs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def pack_drop_dir(app_root: Path) -> Path:
    """Return the repo-local folder users can drag packs into."""
    path = app_root / DROP_FOLDER_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def bundled_pack_dir(app_root: Path) -> Path:
    """Return the bundled starter-pack folder shipped with the app."""
    return app_root / BUNDLED_PACK_FOLDER_NAME


def seed_bundled_packs(app_root: Path) -> list[PackItem]:
    """Copy bundled starter packs into the user's saved library once."""
    seeded: list[PackItem] = []
    try:
        folder = bundled_pack_dir(app_root)
        if not folder.exists():
            return seeded

        library = pack_library_dir()
        existing_names = {path.name.lower() for path in library.iterdir() if path.is_file()}

        for source in sorted(folder.iterdir()):
            if source.suffix.lower() not in ALLOWED_PACK_EXTENSIONS:
                continue
            if source.name.lower() in existing_names:
                continue
            target = library / source.name
            shutil.copy2(source, target)
            seeded.append(pack_from_path(target))
        return seeded
    except Exception:
        logger.exception("failed to seed bundled packs")
        raise


def import_pack_file(source: Path) -> PackItem:
    """Copy a pack file into the saved pack library."""
    try:
        if source.suffix.lower() not in ALLOWED_PACK_EXTENSIONS:
            raise ValueError(f"Unsupported pack type: {source.suffix}")
        if not source.exists():
            raise FileNotFoundError(f"Pack not found: {source}")

        target = unique_target_path(pack_library_dir() / source.name)
        shutil.copy2(source, target)
        return pack_from_path(target)
    except Exception:
        logger.exception("failed to import pack")
        raise


def import_drop_folder(app_root: Path) -> list[PackItem]:
    """Import all supported files from 3_DROP_PACKS_HERE."""
    imported: list[PackItem] = []
    try:
        for path in sorted(pack_drop_dir(app_root).iterdir()):
            if path.is_file() and path.suffix.lower() in ALLOWED_PACK_EXTENSIONS:
                imported.append(import_pack_file(path))
        return imported
    except Exception:
        logger.exception("failed to import drop folder")
        raise


def list_saved_packs() -> list[PackItem]:
    """List saved packs from AppData."""
    try:
        packs = []
        for path in sorted(pack_library_dir().iterdir()):
            if path.is_file() and path.suffix.lower() in ALLOWED_PACK_EXTENSIONS:
                packs.append(pack_from_path(path))
        return packs
    except Exception:
        logger.exception("failed to list packs")
        raise


def load_pack_text(pack: PackItem) -> str:
    """Load saved pack text without executing it."""
    try:
        return pack.path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        logger.exception("failed to load pack text")
        raise


def pack_from_path(path: Path) -> PackItem:
    """Create a PackItem from a file path and optional metadata comments."""
    title = path.stem.replace("_", " ").replace("-", " ").title()
    speed = "normal"
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:12]:
            lower = line.strip().lower()
            if lower.startswith("# title:"):
                title = line.split(":", 1)[1].strip() or title
            if lower.startswith("# recommended_speed:"):
                speed = line.split(":", 1)[1].strip().lower() or speed
    except Exception:
        logger.exception("failed to read pack metadata")
    return PackItem(title=title, path=path, recommended_speed=speed)


def unique_target_path(target: Path) -> Path:
    """Avoid overwriting an existing saved pack."""
    if not target.exists():
        return target
    for index in range(2, 1000):
        candidate = target.with_name(f"{target.stem}-{index}{target.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("Could not create unique pack filename")

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger("nerd_scroll.config")


@dataclass(frozen=True)
class AppSettings:
    name: str
    version: str
    safe_mode: bool


@dataclass(frozen=True)
class TypingSettings:
    base_delay_ms: int
    jitter_ms: int
    line_pause_ms: int
    enable_typos: bool
    typo_chance: float


@dataclass(frozen=True)
class SourceSettings:
    loop_forever: bool
    skip_empty_lines: bool
    allowed_extensions: list[str]


@dataclass(frozen=True)
class DropZoneSettings:
    folder_path: str
    pick_mode: str
    recursive: bool


@dataclass(frozen=True)
class DisplaySettings:
    theme: str
    show_line_numbers: bool
    show_loop_message: bool
    clear_screen_on_start: bool
    show_source_file: bool


@dataclass(frozen=True)
class Settings:
    app: AppSettings
    typing: TypingSettings
    source: SourceSettings
    drop_zone: DropZoneSettings
    display: DisplaySettings


def load_settings(path: Path) -> Settings:
    """Load settings.json and validate it before runtime."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        settings = Settings(
            app=AppSettings(**raw["app"]),
            typing=TypingSettings(**raw["typing"]),
            source=SourceSettings(**raw["source"]),
            drop_zone=DropZoneSettings(**raw["drop_zone"]),
            display=DisplaySettings(**raw["display"]),
        )
        validate_settings(settings)
        return settings
    except Exception:
        logger.exception("failed to load settings")
        raise


def validate_settings(settings: Settings) -> None:
    """Fail early if settings are unsafe or unusable."""
    try:
        if not settings.app.safe_mode:
            raise ValueError("safe_mode must stay true")
        if not 0 <= settings.typing.typo_chance <= 1:
            raise ValueError("typo_chance must be between 0 and 1")
        if settings.drop_zone.pick_mode != "newest":
            raise ValueError("Only pick_mode='newest' is supported")
        if not settings.source.allowed_extensions:
            raise ValueError("At least one extension is required")
    except Exception:
        logger.exception("settings validation failed")
        raise

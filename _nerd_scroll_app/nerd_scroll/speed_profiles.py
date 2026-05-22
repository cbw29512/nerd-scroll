from __future__ import annotations

from dataclasses import dataclass

from nerd_scroll.config import TypingSettings


@dataclass(frozen=True)
class SpeedProfile:
    """User-facing speed profile mapped to typing engine settings."""

    key: str
    label: str
    typing: TypingSettings


PROFILES: dict[str, SpeedProfile] = {
    "super_slow": SpeedProfile("super_slow", "Super slow", TypingSettings(140, 220, 1400, True, 0.004)),
    "slow": SpeedProfile("slow", "Slow", TypingSettings(95, 160, 950, True, 0.006)),
    "normal": SpeedProfile("normal", "Normal - human typing speed", TypingSettings(55, 95, 650, True, 0.008)),
    "fast": SpeedProfile("fast", "Fast", TypingSettings(22, 45, 250, True, 0.006)),
    "really_fast": SpeedProfile("really_fast", "Really fast", TypingSettings(8, 18, 90, False, 0.0)),
    "hyper": SpeedProfile("hyper", "Hyper speed", TypingSettings(2, 5, 20, False, 0.0)),
    "ludicrous": SpeedProfile("ludicrous", "Ludicrous speed", TypingSettings(0, 0, 0, False, 0.0)),
}


LEGACY_CHOICES = {
    "1": "super_slow",
    "2": "slow",
    "3": "normal",
    "4": "fast",
    "5": "really_fast",
    "6": "hyper",
    "7": "ludicrous",
}


def normalize_speed(value: str | None) -> str:
    """Normalize menu number or speed key into a profile key."""
    if not value:
        return "normal"

    cleaned = value.strip().lower()
    return LEGACY_CHOICES.get(cleaned, cleaned if cleaned in PROFILES else "normal")


def get_profile(value: str | None) -> SpeedProfile:
    """Return a safe speed profile. Defaults to normal."""
    return PROFILES[normalize_speed(value)]


def menu_lines() -> list[str]:
    """Return menu lines for CLI prompt output."""
    return [
        "1. Super slow",
        "2. Slow",
        "3. Normal - human typing speed",
        "4. Fast",
        "5. Really fast",
        "6. Hyper speed",
        "7. Ludicrous speed",
    ]

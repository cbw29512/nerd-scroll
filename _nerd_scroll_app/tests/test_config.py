from pathlib import Path
from nerd_scroll.config import load_settings


def test_load_settings() -> None:
    settings = load_settings(Path("_nerd_scroll_app/settings.json"))
    assert settings.app.version == "1.0.0"
    assert settings.drop_zone.folder_path == "1_DROP_TEXT_FILE_HERE"

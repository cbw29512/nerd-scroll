from pathlib import Path
from nerd_scroll.config import SourceSettings
from nerd_scroll.source_reader import load_source_lines


def test_load_source_lines(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    source.write_text("one\n\ntwo\n", encoding="utf-8")
    settings = SourceSettings(True, True, [".txt"])
    assert load_source_lines(source, settings) == ["one", "two"]

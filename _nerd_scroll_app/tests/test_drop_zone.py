from pathlib import Path
from nerd_scroll.drop_zone import list_supported_files


def test_list_supported_files_ignores_readme(tmp_path: Path) -> None:
    (tmp_path / "README_DROP_FILES_HERE.txt").write_text("ignore", encoding="utf-8")
    keep = tmp_path / "sample.txt"
    keep.write_text("keep", encoding="utf-8")
    (tmp_path / "image.png").write_text("ignore", encoding="utf-8")
    files = list_supported_files(tmp_path, [".txt", ".md"], recursive=False)
    assert files == [keep]

from __future__ import annotations

from pathlib import Path
import tkinter as tk

try:
    from tkinterdnd2 import DND_FILES as DND_FILES
    DND_AVAILABLE = True
except Exception:
    DND_FILES = "DND_Files"
    DND_AVAILABLE = False


def parse_drop_paths(root: tk.Tk, data: str) -> list[Path]:
    """Parse dropped Windows paths from tkinterdnd2 event data."""
    try:
        parts = root.tk.splitlist(data)
        return [Path(part) for part in parts if str(part).strip()]
    except Exception:
        cleaned = data.strip().strip("{}")
        return [Path(cleaned)] if cleaned else []

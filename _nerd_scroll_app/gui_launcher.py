from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from nerd_scroll.app_paths import current_source_path
from nerd_scroll.gui_pack_actions import PackUiActions
from nerd_scroll.speed_profiles import PROFILES


class NerdScrollGui:
    """Windows-friendly paste, pack, drag/drop, and run launcher."""

    def __init__(self, root: tk.Tk, app_root: Path) -> None:
        self.root = root
        self.app_root = app_root
        self.speed_var = tk.StringVar(value="normal")
        self.status_var = tk.StringVar(value="Paste text or drop/load a pack, then start.")
        self.pack_var = tk.StringVar(value="")
        self.text_box: tk.Text
        self.pack_combo: ttk.Combobox
        self.pack_actions = PackUiActions(
            root=root,
            app_root=app_root,
            pack_var=self.pack_var,
            speed_var=self.speed_var,
            status_var=self.status_var,
            get_text_box=lambda: self.text_box,
            get_pack_combo=lambda: self.pack_combo,
        )
        self.root.title("Nerd Scroll")
        self.root.geometry("840x680")
        self.root.minsize(720, 540)
        self._build_ui()
        self.pack_actions.refresh_packs()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Nerd Scroll", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Paste text, load a pack, or drag a pack file into this window.").pack(anchor="w")
        pack_frame = ttk.LabelFrame(frame, text="Saved Packs", padding=8)
        pack_frame.pack(fill="x", pady=10)
        self.pack_combo = ttk.Combobox(pack_frame, textvariable=self.pack_var, state="readonly")
        self.pack_combo.pack(side="left", fill="x", expand=True)
        ttk.Button(pack_frame, text="Load Pack", command=self.pack_actions.load_selected_pack).pack(side="left", padx=4)
        ttk.Button(pack_frame, text="Add Pack File...", command=self.pack_actions.add_pack_file).pack(side="left", padx=4)
        ttk.Button(pack_frame, text="Import Drop Folder", command=self.pack_actions.import_packs).pack(side="left", padx=4)
        ttk.Button(pack_frame, text="Open Pack Folder", command=self.pack_actions.open_pack_folder).pack(side="left")
        self.text_box = tk.Text(frame, wrap="word", height=16, undo=True)
        self.text_box.pack(fill="both", expand=True)
        self.text_box.insert("1.0", "Paste text here, or drag/drop a .nscroll/.txt/.md/.log pack file here...\n")
        speed_frame = ttk.LabelFrame(frame, text="Speed", padding=8)
        speed_frame.pack(fill="x", pady=10)
        for key, profile in PROFILES.items():
            ttk.Radiobutton(speed_frame, text=profile.label, value=key, variable=self.speed_var).pack(anchor="w")
        button_row = ttk.Frame(frame)
        button_row.pack(fill="x", pady=(6, 0))
        ttk.Button(button_row, text="Start Nerd Scroll", command=self.start_runner).pack(side="left")
        ttk.Button(button_row, text="Clear Text", command=self.clear_text).pack(side="left", padx=8)
        ttk.Label(button_row, textvariable=self.status_var).pack(side="left", padx=12)
        self.root.bind("<Control-Return>", lambda _event: self.start_runner())
        self.pack_actions.enable_drag_and_drop([self.root, frame, pack_frame, self.text_box])

    def clear_text(self) -> None:
        self.text_box.delete("1.0", "end")
        self.status_var.set("Text cleared.")

    def start_runner(self) -> None:
        try:
            text = self.text_box.get("1.0", "end-1c")
            if not text.strip():
                messagebox.showwarning("Nerd Scroll", "Paste or load some text first.")
                return
            source_path = current_source_path()
            source_path.write_text(text, encoding="utf-8")
            runner_path = self.app_root / "_nerd_scroll_app" / "runner_cli.py"
            command = ["cmd.exe", "/k", sys.executable, str(runner_path), "--source", str(source_path), "--speed", self.speed_var.get()]
            subprocess.Popen(command, cwd=str(self.app_root), creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.status_var.set("Terminal started. Stop it with Ctrl+C or close it.")
        except Exception as exc:
            logging.getLogger("nerd_scroll.gui").exception("failed to start runner")
            messagebox.showerror("Nerd Scroll error", str(exc))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Nerd Scroll GUI")
    parser.add_argument("--root", default=None)
    return parser.parse_args()


def create_root() -> tk.Tk:
    try:
        from tkinterdnd2 import TkinterDnD  # type: ignore
        return TkinterDnD.Tk()
    except Exception:
        return tk.Tk()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    app_root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    root = create_root()
    NerdScrollGui(root, app_root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

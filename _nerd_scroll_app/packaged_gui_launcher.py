from __future__ import annotations

import argparse
import logging
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from nerd_scroll.app_paths import current_source_path
from nerd_scroll.gui_pack_actions import PackUiActions
from nerd_scroll.pack_library import seed_bundled_packs
from nerd_scroll.runner_process import build_runner_command, resolve_app_root
from nerd_scroll.speed_profiles import PROFILES


class NerdScrollGui:
    """Installed Windows GUI for Nerd Scroll."""

    def __init__(self, root: tk.Tk, app_root: Path) -> None:
        self.root = root
        self.app_root = app_root
        self.speed_var = tk.StringVar(value="normal")
        self.status_var = tk.StringVar(value="Choose a pack or paste text, then start.")
        self.pack_var = tk.StringVar(value="")
        self.text_box: tk.Text
        self.pack_combo: ttk.Combobox
        self.pack_actions = PackUiActions(root, app_root, self.pack_var, self.speed_var, self.status_var, lambda: self.text_box, lambda: self.pack_combo)
        self.root.title("Nerd Scroll")
        self.root.geometry("860x700")
        self.root.minsize(740, 560)
        self._build_ui()
        self._seed_and_refresh_packs()

    def _seed_and_refresh_packs(self) -> None:
        try:
            seeded = seed_bundled_packs(self.app_root)
            self.pack_actions.refresh_packs()
            if seeded:
                self.status_var.set(f"Loaded {len(seeded)} starter pack(s).")
        except Exception as exc:
            logging.getLogger("nerd_scroll.gui").exception("starter pack setup failed")
            messagebox.showerror("Nerd Scroll error", str(exc))

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Nerd Scroll", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Turn text and scene packs into cinematic terminal motion.").pack(anchor="w")
        pack_frame = ttk.LabelFrame(frame, text="Step 1: Choose a pack or add your own", padding=8)
        pack_frame.pack(fill="x", pady=10)
        self.pack_combo = ttk.Combobox(pack_frame, textvariable=self.pack_var, state="readonly")
        self.pack_combo.pack(side="left", fill="x", expand=True)
        ttk.Button(pack_frame, text="Load Pack", command=self.pack_actions.load_selected_pack).pack(side="left", padx=4)
        ttk.Button(pack_frame, text="Add Pack...", command=self.pack_actions.add_pack_file).pack(side="left", padx=4)
        self.text_box = tk.Text(frame, wrap="word", height=18, undo=True)
        self.text_box.pack(fill="both", expand=True)
        self.text_box.insert("1.0", "Load a starter pack above, add a pack, or paste your own text here.\n")
        speed_frame = ttk.LabelFrame(frame, text="Step 2: Choose speed", padding=8)
        speed_frame.pack(fill="x", pady=10)
        for key, profile in PROFILES.items():
            ttk.Radiobutton(speed_frame, text=profile.label, value=key, variable=self.speed_var).pack(anchor="w")
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(6, 0))
        ttk.Button(row, text="START NERD SCROLL", command=self.start_runner).pack(side="left")
        ttk.Button(row, text="Clear", command=self.clear_text).pack(side="left", padx=8)
        ttk.Button(row, text="Open Pack Folder", command=self.pack_actions.open_pack_folder).pack(side="left", padx=8)
        ttk.Label(row, textvariable=self.status_var).pack(side="left", padx=12)
        ttk.Label(frame, text="Stop anytime with Ctrl+C or by closing the terminal window.").pack(anchor="w", pady=(8, 0))
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
            command = build_runner_command(self.app_root, source_path, self.speed_var.get())
            subprocess.Popen(command, cwd=str(self.app_root), creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.status_var.set("Terminal started. Stop it with Ctrl+C or close it.")
        except Exception as exc:
            logging.getLogger("nerd_scroll.gui").exception("runner launch failed")
            messagebox.showerror("Nerd Scroll error", str(exc))


def create_root() -> tk.Tk:
    try:
        from tkinterdnd2 import TkinterDnD  # type: ignore
        return TkinterDnD.Tk()
    except Exception:
        return tk.Tk()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Nerd Scroll")
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = create_root()
    NerdScrollGui(root, resolve_app_root(args.root, __file__))
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

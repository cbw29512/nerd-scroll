from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from nerd_scroll.app_paths import current_source_path
from nerd_scroll.pack_library import import_drop_folder, list_saved_packs, load_pack_text
from nerd_scroll.speed_profiles import PROFILES, normalize_speed


class NerdScrollGui:
    """Windows-friendly paste, pack, and run launcher."""

    def __init__(self, root: tk.Tk, app_root: Path) -> None:
        self.root = root
        self.app_root = app_root
        self.speed_var = tk.StringVar(value="normal")
        self.status_var = tk.StringVar(value="Paste text or load a pack, then start.")
        self.pack_var = tk.StringVar(value="")
        self.saved_packs = []
        self.text_box: tk.Text
        self.pack_combo: ttk.Combobox

        self.root.title("Nerd Scroll")
        self.root.geometry("820x650")
        self.root.minsize(700, 520)
        self._build_ui()
        self.refresh_packs()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Nerd Scroll", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Paste text or load a saved pack. Nerd Scroll reads text only.").pack(anchor="w")

        pack_frame = ttk.LabelFrame(frame, text="Saved Packs", padding=8)
        pack_frame.pack(fill="x", pady=10)
        self.pack_combo = ttk.Combobox(pack_frame, textvariable=self.pack_var, state="readonly")
        self.pack_combo.pack(side="left", fill="x", expand=True)
        ttk.Button(pack_frame, text="Load Pack", command=self.load_selected_pack).pack(side="left", padx=6)
        ttk.Button(pack_frame, text="Import Drop Folder", command=self.import_packs).pack(side="left")

        self.text_box = tk.Text(frame, wrap="word", height=16, undo=True)
        self.text_box.pack(fill="both", expand=True)
        self.text_box.insert("1.0", "Paste your text here, or import/load a pack above...\n")

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

    def refresh_packs(self) -> None:
        try:
            self.saved_packs = list_saved_packs()
            names = [pack.title for pack in self.saved_packs]
            self.pack_combo["values"] = names
            if names and not self.pack_var.get():
                self.pack_var.set(names[0])
            self.status_var.set(f"Saved packs: {len(names)}")
        except Exception as exc:
            messagebox.showerror("Nerd Scroll error", str(exc))

    def import_packs(self) -> None:
        try:
            imported = import_drop_folder(self.app_root)
            self.refresh_packs()
            self.status_var.set(f"Imported {len(imported)} pack(s).")
            if not imported:
                messagebox.showinfo("Nerd Scroll", "No supported pack files found in 3_DROP_PACKS_HERE.")
        except Exception as exc:
            messagebox.showerror("Nerd Scroll error", str(exc))

    def load_selected_pack(self) -> None:
        try:
            selected = self.pack_var.get()
            pack = next((item for item in self.saved_packs if item.title == selected), None)
            if pack is None:
                messagebox.showwarning("Nerd Scroll", "Choose a saved pack first.")
                return
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", load_pack_text(pack))
            self.speed_var.set(normalize_speed(pack.recommended_speed))
            self.status_var.set(f"Loaded pack: {pack.title}")
        except Exception as exc:
            messagebox.showerror("Nerd Scroll error", str(exc))

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


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    app_root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    root = tk.Tk()
    NerdScrollGui(root, app_root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

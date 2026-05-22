from __future__ import annotations

import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from nerd_scroll.gui_dnd import DND_AVAILABLE, DND_FILES, parse_drop_paths
from nerd_scroll.pack_library import (
    ALLOWED_PACK_EXTENSIONS,
    PackItem,
    import_drop_folder,
    import_pack_file,
    list_saved_packs,
    load_pack_text,
    pack_drop_dir,
)
from nerd_scroll.speed_profiles import normalize_speed


class PackUiActions:
    """Pack import/load actions used by the GUI."""

    def __init__(self, root: tk.Tk, app_root: Path, pack_var: tk.StringVar, speed_var: tk.StringVar, status_var: tk.StringVar, get_text_box, get_pack_combo) -> None:
        self.root = root
        self.app_root = app_root
        self.pack_var = pack_var
        self.speed_var = speed_var
        self.status_var = status_var
        self.get_text_box = get_text_box
        self.get_pack_combo = get_pack_combo
        self.saved_packs: list[PackItem] = []
        self.display_map: dict[str, PackItem] = {}

    def refresh_packs(self) -> None:
        self.saved_packs = list_saved_packs()
        self.display_map = {self.display_name(pack): pack for pack in self.saved_packs}
        names = list(self.display_map.keys())
        combo: ttk.Combobox = self.get_pack_combo()
        combo["values"] = names
        if names and self.pack_var.get() not in names:
            self.pack_var.set(names[0])
        self.status_var.set(f"Saved packs: {len(names)}")

    def add_pack_file(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Add Nerd Scroll Pack",
            filetypes=[("Nerd Scroll packs", "*.nscroll *.txt *.md *.log"), ("All files", "*.*")],
        )
        if paths:
            self.import_paths([Path(path) for path in paths])

    def import_packs(self) -> None:
        imported = import_drop_folder(self.app_root)
        self.refresh_packs()
        self.load_import_result(imported, "No supported pack files found in 3_DROP_PACKS_HERE.")

    def import_paths(self, paths: list[Path]) -> None:
        imported = []
        for path in paths:
            if path.suffix.lower() in ALLOWED_PACK_EXTENSIONS:
                imported.append(import_pack_file(path))
        self.refresh_packs()
        self.load_import_result(imported, "No supported .nscroll, .txt, .md, or .log files were selected.")

    def load_import_result(self, imported: list[PackItem], empty_message: str) -> None:
        if not imported:
            messagebox.showinfo("Nerd Scroll", empty_message)
            return
        self.select_and_load(imported[-1])
        self.status_var.set(f"Imported and loaded: {imported[-1].title}")

    def load_selected_pack(self) -> None:
        pack = self.display_map.get(self.pack_var.get())
        if pack is None:
            messagebox.showwarning("Nerd Scroll", "Choose a saved pack first.")
            return
        self.select_and_load(pack)

    def select_and_load(self, pack: PackItem) -> None:
        box: tk.Text = self.get_text_box()
        box.delete("1.0", "end")
        box.insert("1.0", load_pack_text(pack))
        display = self.display_name(pack)
        self.pack_var.set(display)
        self.speed_var.set(normalize_speed(pack.recommended_speed))
        self.status_var.set(f"Loaded pack: {pack.title}")

    def open_pack_folder(self) -> None:
        folder = pack_drop_dir(self.app_root)
        try:
            os.startfile(str(folder))
        except Exception as exc:
            messagebox.showerror("Nerd Scroll error", str(exc))

    def enable_drag_and_drop(self, widgets: list[tk.Misc]) -> None:
        if not DND_AVAILABLE:
            self.status_var.set("Tip: use Add Pack File or Import Drop Folder.")
            return
        for widget in widgets:
            try:
                widget.drop_target_register(DND_FILES)
                widget.dnd_bind("<<Drop>>", self.handle_drop)
            except Exception:
                continue

    def handle_drop(self, event) -> None:
        paths = parse_drop_paths(self.root, event.data)
        self.import_paths(paths)

    @staticmethod
    def display_name(pack: PackItem) -> str:
        return f"{pack.title} — {pack.path.name}"

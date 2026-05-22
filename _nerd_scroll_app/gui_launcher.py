from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from nerd_scroll.app_paths import current_source_path
from nerd_scroll.speed_profiles import PROFILES


class NerdScrollGui:
    """Tiny Windows-friendly paste-and-run launcher."""

    def __init__(self, root: tk.Tk, app_root: Path) -> None:
        self.root = root
        self.app_root = app_root
        self.speed_var = tk.StringVar(value="normal")
        self.status_var = tk.StringVar(value="Paste text, pick speed, then start.")
        self.text_box: tk.Text

        self.root.title("Nerd Scroll")
        self.root.geometry("760x560")
        self.root.minsize(640, 460)
        self._build_ui()

    def _build_ui(self) -> None:
        """Create the visible Windows controls."""
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nerd Scroll", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text="Paste text, code, logs, or notes below. Nerd Scroll reads text only.",
        ).pack(anchor="w", pady=(0, 10))

        self.text_box = tk.Text(frame, wrap="word", height=16, undo=True)
        self.text_box.pack(fill="both", expand=True)
        self.text_box.insert("1.0", "Paste your text here...\n")

        speed_frame = ttk.LabelFrame(frame, text="Speed", padding=8)
        speed_frame.pack(fill="x", pady=10)

        for key, profile in PROFILES.items():
            ttk.Radiobutton(
                speed_frame,
                text=profile.label,
                value=key,
                variable=self.speed_var,
            ).pack(anchor="w")

        button_row = ttk.Frame(frame)
        button_row.pack(fill="x", pady=(6, 0))

        ttk.Button(button_row, text="Start Nerd Scroll", command=self.start_runner).pack(side="left")
        ttk.Button(button_row, text="Clear Text", command=self.clear_text).pack(side="left", padx=8)
        ttk.Label(button_row, textvariable=self.status_var).pack(side="left", padx=12)

        self.root.bind("<Control-Return>", lambda _event: self.start_runner())

    def clear_text(self) -> None:
        """Clear the input box."""
        self.text_box.delete("1.0", "end")
        self.status_var.set("Text cleared.")

    def start_runner(self) -> None:
        """Save pasted text and launch terminal runner in a new window."""
        try:
            text = self.text_box.get("1.0", "end-1c")

            if not text.strip():
                messagebox.showwarning("Nerd Scroll", "Paste some text first.")
                return

            source_path = current_source_path()
            source_path.write_text(text, encoding="utf-8")

            runner_path = self.app_root / "_nerd_scroll_app" / "runner_cli.py"
            speed = self.speed_var.get()

            command = [
                "cmd.exe",
                "/k",
                sys.executable,
                str(runner_path),
                "--source",
                str(source_path),
                "--speed",
                speed,
            ]

            subprocess.Popen(
                command,
                cwd=str(self.app_root),
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.status_var.set("Terminal started. Stop it with Ctrl+C or close it.")
        except Exception as exc:
            logging.getLogger("nerd_scroll.gui").exception("failed to start runner")
            messagebox.showerror("Nerd Scroll error", str(exc))


def parse_args() -> argparse.Namespace:
    """Parse GUI launcher args."""
    parser = argparse.ArgumentParser(description="Nerd Scroll GUI")
    parser.add_argument("--root", default=None)
    return parser.parse_args()


def main() -> int:
    """Start the GUI."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    app_root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]

    root = tk.Tk()
    NerdScrollGui(root, app_root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

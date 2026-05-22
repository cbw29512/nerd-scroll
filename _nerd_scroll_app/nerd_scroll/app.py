from __future__ import annotations

import logging
import os
from pathlib import Path

from nerd_scroll.config import Settings
from nerd_scroll.state import RuntimeState
from nerd_scroll.terminal_writer import TerminalWriter


logger = logging.getLogger("nerd_scroll.app")


class NerdScrollApp:
    """Coordinate settings, source text, state, and terminal output."""

    def __init__(
        self,
        settings: Settings,
        source_lines: list[str],
        source_path: Path,
        max_lines: int = 0,
        instant: bool = False,
    ) -> None:
        self.settings = settings
        self.source_lines = source_lines
        self.max_lines = max_lines
        self.writer = TerminalWriter(settings.typing, settings.display, instant)
        self.state = RuntimeState(str(source_path), len(source_lines))

    def run(self) -> None:
        """Run until Ctrl+C or until max_lines is reached."""
        try:
            self._show_startup()
            while self.state.is_running:
                if self.max_lines and self.state.lines_typed >= self.max_lines:
                    break
                self._write_next_line()
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            self.state.last_error = str(exc)
            logger.exception("app loop failed")
            raise
        finally:
            self._show_shutdown()

    def _write_next_line(self) -> None:
        """Write one source line, then advance state."""
        try:
            rewound = self.state.rewind_if_needed()
            if rewound and self.settings.display.show_loop_message:
                self.writer.write_line(f"[loop {self.state.loop_count}] Reached end. Rewinding...")

            index = self.state.current_line_index
            line = self.source_lines[index]
            visible = f"{index + 1:04d} | {line}" if self.settings.display.show_line_numbers else line
            chars = self.writer.write_line(visible)
            self.state.characters_typed += chars
            self.state.advance_line()
        except Exception:
            logger.exception("failed to write next source line")
            raise

    def _show_startup(self) -> None:
        """Show a friendly startup message."""
        try:
            if self.settings.display.clear_screen_on_start:
                os.system("cls" if os.name == "nt" else "clear")
            print(f"{self.settings.app.name} v{self.settings.app.version}")
            print("Two Step Edition")
            print("Stage 1: drop a file in 1_DROP_TEXT_FILE_HERE")
            print("Stage 2: run 2_RUN_NERD_SCROLL.bat")
            print("Dropped files are read as text, not executed.")
            if self.settings.display.show_source_file:
                print(f"Source: {self.state.source_path}")
            print("Stop: Ctrl+C\n")
        except Exception:
            logger.exception("startup message failed")
            raise

    def _show_shutdown(self) -> None:
        """Show a short local-only summary."""
        try:
            print("\nNerd Scroll shutdown.")
            print(f"Lines typed: {self.state.lines_typed}")
            print(f"Characters typed: {self.state.characters_typed}")
            print(f"Loops completed: {self.state.loop_count}")
            print("No real actions were performed.")
        except Exception:
            logger.exception("shutdown message failed")

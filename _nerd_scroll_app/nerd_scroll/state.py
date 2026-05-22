from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RuntimeState:
    """Mutable runtime state for the typing loop."""

    source_path: str
    source_line_count: int
    current_line_index: int = 0
    loop_count: int = 0
    lines_typed: int = 0
    characters_typed: int = 0
    started_at: datetime = field(default_factory=datetime.now)
    is_running: bool = True
    last_error: str | None = None

    def advance_line(self) -> None:
        """Move to the next source line after rendering it."""
        try:
            self.current_line_index += 1
            self.lines_typed += 1
        except Exception as exc:
            self.last_error = str(exc)
            raise

    def rewind_if_needed(self) -> bool:
        """Loop back to the top when the source reaches the end."""
        try:
            if self.current_line_index < self.source_line_count:
                return False
            self.current_line_index = 0
            self.loop_count += 1
            return True
        except Exception as exc:
            self.last_error = str(exc)
            raise

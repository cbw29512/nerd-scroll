from __future__ import annotations

import logging
import random
import sys
import time

from nerd_scroll.config import DisplaySettings, TypingSettings


logger = logging.getLogger("nerd_scroll.terminal_writer")


ANSI = {
    "green": "\033[92m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "amber": "\033[93m",
    "reset": "\033[0m",
}


class TerminalWriter:
    """Render text with a human-like typing effect."""

    def __init__(self, typing: TypingSettings, display: DisplaySettings, instant: bool = False) -> None:
        self.typing = typing
        self.display = display
        self.instant = instant

    def write_line(self, text: str) -> int:
        """Type one line and return the number of characters rendered."""
        try:
            color = ANSI.get(self.display.theme, ANSI["green"])
            reset = ANSI["reset"]

            if self.instant:
                print(f"{color}{text}{reset}")
                return len(text)

            sys.stdout.write(color)
            count = 0
            for char in text:
                self._maybe_typo(char)
                sys.stdout.write(char)
                sys.stdout.flush()
                count += 1
                time.sleep(self._char_delay(char))

            sys.stdout.write(reset + "\n")
            sys.stdout.flush()
            time.sleep(self.typing.line_pause_ms / 1000)
            return count
        except Exception:
            logger.exception("failed while writing terminal line")
            raise

    def _char_delay(self, char: str) -> float:
        """Calculate a human-ish delay for each typed character."""
        try:
            jitter = random.randint(0, self.typing.jitter_ms)
            if char in ".:,;)]}":
                jitter += random.randint(20, 120)
            if char == " ":
                jitter += random.randint(0, 25)
            return max(0, self.typing.base_delay_ms + jitter) / 1000
        except Exception:
            logger.exception("failed to calculate character delay")
            return 0.025

    def _maybe_typo(self, char: str) -> None:
        """Occasionally type a wrong letter, then backspace it."""
        try:
            if self.instant or not self.typing.enable_typos or not char.isalpha():
                return
            if random.random() > self.typing.typo_chance:
                return

            wrong = random.choice("abcdefghijklmnopqrstuvwxyz")
            sys.stdout.write(wrong)
            sys.stdout.flush()
            time.sleep(random.uniform(0.05, 0.18))
            sys.stdout.write("\b \b")
            sys.stdout.flush()
        except Exception:
            logger.exception("typo simulation failed safely")

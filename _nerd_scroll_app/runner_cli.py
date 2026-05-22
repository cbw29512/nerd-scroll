from __future__ import annotations

import argparse
import logging
from pathlib import Path

from nerd_scroll.config import DisplaySettings
from nerd_scroll.source_reader import load_source_lines
from nerd_scroll.speed_profiles import get_profile
from nerd_scroll.terminal_writer import TerminalWriter


class RunnerSourceSettings:
    """Minimal source settings used by the terminal runner."""

    def __init__(self, suffix: str) -> None:
        self.skip_empty_lines = False
        self.allowed_extensions = [suffix.lower() or ".txt"]


def parse_args() -> argparse.Namespace:
    """Parse runner options sent by the GUI."""
    parser = argparse.ArgumentParser(description="Nerd Scroll terminal runner.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--speed", default="normal")
    parser.add_argument("--max-lines", type=int, default=0)
    parser.add_argument("--instant", action="store_true")
    return parser.parse_args()


def run_loop(source: Path, speed: str, max_lines: int, instant: bool) -> int:
    """Read source text and type it forever until Ctrl+C."""
    logger = logging.getLogger("nerd_scroll.runner_cli")

    try:
        profile = get_profile(speed)
        display = DisplaySettings("green", True, True, False, True)
        lines = load_source_lines(source, RunnerSourceSettings(source.suffix))
        writer = TerminalWriter(profile.typing, display, instant)

        print("Nerd Scroll terminal runner")
        print(f"Source: {source}")
        print(f"Speed: {profile.label}")
        print("Stop: Ctrl+C or close this window.")
        print("")

        index = 0
        loops = 0
        typed = 0

        while True:
            if max_lines and typed >= max_lines:
                break

            if index >= len(lines):
                index = 0
                loops += 1
                writer.write_line(f"[loop {loops}] Reached end. Rewinding...")

            visible = f"{index + 1:04d} | {lines[index]}"
            writer.write_line(visible)
            index += 1
            typed += 1

        return 0
    except KeyboardInterrupt:
        print("\nNerd Scroll stopped. No real actions were performed.")
        return 0
    except Exception as exc:
        logger.exception("runner failed")
        print(f"\nERROR: {exc}")
        return 1


def main() -> int:
    """Runner entrypoint."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    return run_loop(Path(args.source), args.speed, args.max_lines, args.instant)


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import logging
from dataclasses import replace
from pathlib import Path

from nerd_scroll.app import NerdScrollApp
from nerd_scroll.config import TypingSettings, load_settings
from nerd_scroll.drop_zone import find_drop_zone_source
from nerd_scroll.source_reader import load_source_lines


SPEED_PROFILES: dict[str, tuple[str, TypingSettings]] = {
    "1": ("super slow", TypingSettings(140, 220, 1400, True, 0.004)),
    "2": ("slow", TypingSettings(95, 160, 950, True, 0.006)),
    "3": ("normal - human typing speed", TypingSettings(55, 95, 650, True, 0.008)),
    "4": ("fast", TypingSettings(22, 45, 250, True, 0.006)),
    "5": ("really fast", TypingSettings(8, 18, 90, False, 0.0)),
    "6": ("ludicrous speed", TypingSettings(0, 2, 0, False, 0.0)),
}


def parse_args() -> argparse.Namespace:
    """Parse command-line options before app state is built."""
    parser = argparse.ArgumentParser(description="Nerd Scroll launcher.")
    parser.add_argument("--root", default=None)
    parser.add_argument("--settings", default="_nerd_scroll_app/settings.json")
    parser.add_argument("--source", default=None)
    parser.add_argument("--drop-zone", action="store_true")
    parser.add_argument("--max-lines", type=int, default=0)
    parser.add_argument("--instant", action="store_true")
    parser.add_argument("--speed", choices=["1", "2", "3", "4", "5", "6"], default=None)
    return parser.parse_args()


def resolve_root(args: argparse.Namespace) -> Path:
    """Use the repo folder as root instead of guessing from the hidden app folder."""
    try:
        if args.root:
            return Path(args.root).resolve()

        return Path(__file__).resolve().parents[1]
    except Exception:
        logging.getLogger("nerd_scroll").exception("failed to resolve root")
        raise


def choose_speed() -> str:
    """Ask the user for speed in normal double-click mode."""
    try:
        print("")
        print("Choose Nerd Scroll speed:")
        print("")
        print("  1. Super slow")
        print("  2. Slow")
        print("  3. Normal - human typing speed")
        print("  4. Fast")
        print("  5. Really fast")
        print("  6. Ludicrous speed")
        print("")

        choice = input("Pick 1-6, then press Enter [3]: ").strip()

        if not choice:
            return "3"

        if choice not in SPEED_PROFILES:
            print("Unknown choice. Using normal human typing speed.")
            return "3"

        return choice
    except Exception:
        logging.getLogger("nerd_scroll").exception("speed prompt failed")
        return "3"


def apply_speed(settings, choice: str):
    """Return a settings copy with the selected runtime speed applied."""
    try:
        label, typing_settings = SPEED_PROFILES.get(choice, SPEED_PROFILES["3"])
        print(f"Speed selected: {label}")
        return replace(settings, typing=typing_settings)
    except Exception:
        logging.getLogger("nerd_scroll").exception("failed to apply speed")
        raise


def main() -> int:
    """Load schema/state first, then run the terminal renderer."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("nerd_scroll")

    try:
        args = parse_args()
        root = resolve_root(args)
        settings = load_settings(root / args.settings)

        speed_choice = args.speed
        if speed_choice is None and not args.instant:
            speed_choice = choose_speed()

        settings = apply_speed(settings, speed_choice or "3")

        if args.source:
            source_path = (root / args.source).resolve()
        else:
            source_path = find_drop_zone_source(root, settings)

        source_lines = load_source_lines(source_path, settings.source)

        app = NerdScrollApp(
            settings=settings,
            source_lines=source_lines,
            source_path=source_path,
            max_lines=args.max_lines,
            instant=args.instant,
        )
        app.run()
        return 0
    except KeyboardInterrupt:
        print("\nNerd Scroll stopped by user. No real actions were performed.")
        return 0
    except Exception as exc:
        logger.exception("Nerd Scroll failed")
        print(f"\nERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

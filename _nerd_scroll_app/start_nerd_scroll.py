from __future__ import annotations

import argparse
import logging
from dataclasses import replace
from pathlib import Path

from nerd_scroll.app import NerdScrollApp
from nerd_scroll.config import load_settings
from nerd_scroll.drop_zone import find_drop_zone_source
from nerd_scroll.source_reader import load_source_lines
from nerd_scroll.speed_profiles import get_profile, menu_lines, normalize_speed


def parse_args() -> argparse.Namespace:
    """Parse command-line options before app state is built."""
    parser = argparse.ArgumentParser(description="Nerd Scroll legacy drop-zone launcher.")
    parser.add_argument("--root", default=None)
    parser.add_argument("--settings", default="_nerd_scroll_app/settings.json")
    parser.add_argument("--source", default=None)
    parser.add_argument("--drop-zone", action="store_true")
    parser.add_argument("--max-lines", type=int, default=0)
    parser.add_argument("--instant", action="store_true")
    parser.add_argument("--speed", default=None)
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
        for line in menu_lines():
            print(f"  {line}")
        print("")
        choice = input("Pick 1-6, then press Enter [3]: ").strip()
        return normalize_speed(choice or "3")
    except Exception:
        logging.getLogger("nerd_scroll").exception("speed prompt failed")
        return "normal"


def apply_speed(settings, choice: str):
    """Return a settings copy with the selected runtime speed applied."""
    try:
        profile = get_profile(choice)
        print(f"Speed selected: {profile.label}")
        return replace(settings, typing=profile.typing)
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

        settings = apply_speed(settings, speed_choice or "normal")

        if args.source:
            source_path = (root / args.source).resolve()
        else:
            source_path = find_drop_zone_source(root, settings)

        source_lines = load_source_lines(source_path, settings.source)
        app = NerdScrollApp(settings, source_lines, source_path, args.max_lines, args.instant)
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

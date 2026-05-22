from __future__ import annotations

import argparse
import logging
from pathlib import Path

from nerd_scroll.app import NerdScrollApp
from nerd_scroll.config import load_settings
from nerd_scroll.drop_zone import find_drop_zone_source
from nerd_scroll.source_reader import load_source_lines


def parse_args() -> argparse.Namespace:
    """Parse user-friendly command-line options."""
    parser = argparse.ArgumentParser(description="Nerd Scroll launcher.")
    parser.add_argument("--root", default=None)
    parser.add_argument("--settings", default="_nerd_scroll_app/settings.json")
    parser.add_argument("--source", default=None)
    parser.add_argument("--drop-zone", action="store_true")
    parser.add_argument("--max-lines", type=int, default=0)
    parser.add_argument("--instant", action="store_true")
    return parser.parse_args()


def resolve_root(args: argparse.Namespace) -> Path:
    """Use launcher folder as the app root, not the hidden app folder."""
    try:
        if args.root:
            return Path(args.root).resolve()
        return Path(__file__).resolve().parents[1]
    except Exception:
        logging.getLogger("nerd_scroll").exception("failed to resolve root")
        raise


def main() -> int:
    """Load schema/state first, then run the terminal renderer."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("nerd_scroll")

    try:
        args = parse_args()
        root = resolve_root(args)
        settings = load_settings(root / args.settings)

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

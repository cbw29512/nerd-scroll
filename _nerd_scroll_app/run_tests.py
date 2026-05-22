from __future__ import annotations

import importlib.util
import tempfile
import traceback
from pathlib import Path


def run() -> int:
    failures = 0
    for path in sorted(Path("_nerd_scroll_app/tests").glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)

        try:
            assert spec and spec.loader
            spec.loader.exec_module(module)
            for name in dir(module):
                if not name.startswith("test_"):
                    continue
                func = getattr(module, name)
                if "tmp_path" in func.__code__.co_varnames:
                    with tempfile.TemporaryDirectory() as td:
                        func(Path(td))
                else:
                    func()
            print(f"PASS {path}")
        except Exception:
            failures += 1
            print(f"FAIL {path}")
            traceback.print_exc()
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run())

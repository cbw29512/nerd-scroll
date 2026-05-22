# Nerd Scroll

Nerd Scroll turns any dropped text, code, or log file into a human-typing terminal stream.

## Two-step workflow

1. Drop a supported file into `1_DROP_TEXT_FILE_HERE/`.
2. Double-click `2_RUN_NERD_SCROLL.bat`.

Nerd Scroll automatically picks the newest supported file in the drop folder and types it into the command line. When it reaches the end, it loops back to the top.

## Supported files

`.txt`, `.log`, `.md`, `.py`, `.js`, `.ts`, `.ps1`, `.json`, `.sql`, `.html`, `.css`, `.xml`, `.yaml`, `.yml`, `.cbl`, `.jcl`

## Stop

Press `Ctrl+C` in the command window.

## Safety

Nerd Scroll reads dropped files as text only. It does not execute dropped code, use the internet, run Git, run Docker, install packages, publish anything, or touch credentials.

## Developer test

```powershell
python _nerd_scroll_app/run_tests.py
python _nerd_scroll_app/start_nerd_scroll.py --root . --drop-zone --max-lines 30 --instant
```

## Version

Current release: `v0.3.0-two-step`

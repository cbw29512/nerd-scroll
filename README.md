# Nerd Scroll

Nerd Scroll turns pasted text, code, logs, notes, and reusable source packs into a cinematic terminal typing stream.

## Windows GUI workflow

1. Double-click `2_RUN_NERD_SCROLL.bat`.
2. Paste text into the window, or load a saved pack.
3. Pick a speed.
4. Click **Start Nerd Scroll**.
5. A command-line window opens and types your text forever.

Stop the stream with `Ctrl+C` or by closing the command-line window.

## Pack library workflow

1. Put `.txt`, `.md`, `.log`, or `.nscroll` pack files into `3_DROP_PACKS_HERE/`.
2. Open Nerd Scroll.
3. Click **Import Drop Folder**.
4. Pick the saved pack from the dropdown.
5. Click **Load Pack**.
6. Click **Start Nerd Scroll**.

Imported packs are copied into your local AppData pack library for easy reuse.

Pack files can include optional metadata at the top:

```text
# title: Cyber City Mural
# recommended_speed: slow
```

Supported recommended speeds: `super_slow`, `slow`, `normal`, `fast`, `really_fast`, `ludicrous`.

## Speed choices

- Super slow
- Slow
- Normal - human typing speed
- Fast
- Really fast
- Ludicrous speed

## Desktop shortcut

Run:

```powershell
.\INSTALL_DESKTOP_SHORTCUT.bat
```

This creates a `Nerd Scroll` desktop shortcut.

## Legacy drop-zone mode

The original drop-zone workflow is still available:

```powershell
.\RUN_DROP_ZONE_LEGACY.bat
```

## Safety

Nerd Scroll reads pasted, dropped, and imported pack text only. It does not execute pasted code, use the internet, run Git, run Docker, install packages, publish anything, or touch credentials.

## Developer tests

```powershell
python _nerd_scroll_app\run_tests.py
python _nerd_scroll_app\runner_cli.py --source 1_DROP_TEXT_FILE_HERE\example_to_replace.txt --speed ludicrous --max-lines 5 --instant
```

## Version

Current release: `v0.6.0-pack-library`

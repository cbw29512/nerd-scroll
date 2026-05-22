# Nerd Scroll

Nerd Scroll turns pasted text, code, logs, notes, and reusable source packs into a cinematic terminal typing stream.

## Windows GUI workflow

1. Double-click `2_RUN_NERD_SCROLL.bat`.
2. Paste text, load a saved pack, or drop a pack file into the window.
3. Pick a speed.
4. Click **Start Nerd Scroll**.
5. A command-line window opens and types your text forever.

Stop the stream with `Ctrl+C` or by closing the command-line window.

## Pack workflow

Users can add packs three ways:

1. **Drag and drop:** drag a `.txt`, `.md`, `.log`, or `.nscroll` pack into the Nerd Scroll window.
2. **Add Pack File:** click **Add Pack File...** and choose a pack from Downloads.
3. **Drop folder:** put packs into `3_DROP_PACKS_HERE/`, then click **Import Drop Folder**.

Imported packs are copied into your local AppData pack library for easy reuse. After import, choose the pack from the dropdown and click **Load Pack**.

True drag-and-drop requires the optional drag-drop helper. Run this once:

```powershell
.\INSTALL_DRAG_DROP_SUPPORT.bat
```

If that is not installed, Nerd Scroll still works with **Add Pack File...** and **Import Drop Folder**.

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

Current release: `v0.7.0-pack-drop-ux`

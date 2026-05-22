# Nerd Scroll Release Audit v0.8

## Objective

Tighten Nerd Scroll into a cleaner paid-app beta before adding more features.

Current business target:

```text
Nerd Scroll app: $4.99
Included starter packs: 3
Individual premium packs: $0.99
10-pack bundles: $4.99
```

---

## Current Architecture

```text
2_RUN_NERD_SCROLL.bat
  -> _nerd_scroll_app/gui_launcher.py
     -> GUI paste/load/import screen
     -> AppData current_source.txt handoff
     -> _nerd_scroll_app/runner_cli.py
        -> terminal typing loop

bundled_packs/
  -> starter packs copied into AppData pack library on first launch

3_DROP_PACKS_HERE/
  -> user drop/import folder for packs
```

---

## State / Data Schema

### Runtime handoff

```text
AppData/Local/NerdScroll/current_source.txt
```

This file stores the text currently loaded in the GUI. The terminal runner reads it as plain text only.

### Saved pack library

```text
AppData/Local/NerdScroll/packs/
```

Imported packs and bundled starter packs are copied here for easy reuse.

### Pack metadata

```text
# title: Cyber City Starter
# recommended_speed: slow
# category: cyberpunk terminal art
# creator: Nerd Scroll
# license: included starter pack
```

---

## Audit Findings

### Fixed: bundled starter packs did not show in dropdown

Issue:

```text
bundled_packs existed, but gui_launcher.py called refresh_packs() directly.
```

Fix:

```text
gui_launcher.py now calls _seed_and_refresh_packs(), which runs seed_bundled_packs(app_root) before refreshing the Saved Packs dropdown.
```

### Fixed: duplicated speed profile logic

Issue:

```text
Legacy start_nerd_scroll.py had its own SPEED_PROFILES table even though shared speed_profiles.py exists.
```

Fix:

```text
Legacy launcher now imports get_profile(), menu_lines(), and normalize_speed() from nerd_scroll.speed_profiles.
```

### Good: no __pycache__ found in repository search

Repo search did not find committed `__pycache__` entries during audit.

---

## Remaining Release Cleanup

### Must do before paid beta

```text
[ ] Pull latest repo locally
[ ] Run unit tests locally
[ ] Run GUI locally
[ ] Confirm 3 bundled packs appear in dropdown
[ ] Confirm each starter pack loads
[ ] Confirm recommended speed changes when pack loads
[ ] Confirm Start Nerd Scroll opens terminal runner
[ ] Confirm Ctrl+C stops runner
[ ] Confirm Add Pack File works
[ ] Confirm Import Drop Folder works
[ ] Confirm optional drag/drop helper path is documented
```

### Should do next

```text
[ ] Restore/add DIY_PACK_CREATOR_GUIDE.md if missing
[ ] Add release ZIP builder
[ ] Add clean customer ZIP output
[ ] Exclude .git, __pycache__, _patch_backups, and runtime folders from release ZIP
[ ] Add Windows install/readme instructions for non-coders
[ ] Package EXE after ZIP beta works
```

---

## Safety Review

Nerd Scroll should remain cosmetic only.

Allowed:

```text
- Read pasted text
- Read imported packs
- Save pack text locally
- Type text into terminal
- Loop text forever
```

Not allowed:

```text
- Execute pasted code
- Execute pack content
- Read credentials
- Run Git from the app
- Run Docker from the app
- Use internet/network from the app
- Publish or upload anything
```

---

## Production Recommendation

Do not add new features until v0.8 local validation passes.

Next best milestone:

```text
v0.8 Customer ZIP Beta
```

Definition of done:

```text
A clean zipped folder that a Windows user can unzip, run, load the three starter packs, import a pack, and start the terminal stream without opening PowerShell.
```

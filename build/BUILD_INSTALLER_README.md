# Nerd Scroll Windows Installer Build

## Goal

Create a Windows installer that a customer can download, run, and use without opening the source repo.

## Build Stack

- PyInstaller builds the GUI and runner executables.
- Inno Setup builds the final installer EXE.

## Output

```text
release/NerdScrollSetup-v1.0.0.exe
```

## Required Local Tools

Install once on the build machine:

```powershell
python -m pip install -r requirements-build.txt
```

Install Inno Setup and make sure ISCC.exe is available from:

```text
C:\Program Files (x86)\Inno Setup 6\ISCC.exe
```

## Build Command

```powershell
powershell -ExecutionPolicy Bypass -File .\build\build_windows_installer.ps1
```

## Customer Result

The installer should create:

- Program Files app folder
- Start Menu shortcut
- Optional Desktop shortcut
- Bundled starter packs
- Pack drop folder
- GUI app launcher
- Terminal runner executable

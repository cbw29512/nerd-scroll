@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0INSTALL_DESKTOP_SHORTCUT.ps1"
pause

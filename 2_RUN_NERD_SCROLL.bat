@echo off
title Nerd Scroll
cd /d "%~dp0"

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python "_nerd_scroll_app\gui_launcher.py" --root .
    goto done
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py "_nerd_scroll_app\gui_launcher.py" --root .
    goto done
)

echo ERROR: Python was not found on this computer.
echo.
echo Install Python from:
echo   https://www.python.org/downloads/
echo.
echo During install, check:
echo   Add python.exe to PATH
echo.
pause
exit /b 1

:done

@echo off
title Nerd Scroll - Install Drag and Drop Support
cd /d "%~dp0"

echo Installing optional drag-and-drop support for Nerd Scroll...
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python -m pip install -r requirements.txt
    goto done
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -m pip install -r requirements.txt
    goto done
)

echo ERROR: Python was not found on this computer.
pause
exit /b 1

:done
echo.
echo If install succeeded, restart Nerd Scroll.
pause

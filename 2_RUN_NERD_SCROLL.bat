@echo off
title Nerd Scroll - Two Step Edition
cd /d "%~dp0"

echo ============================================================
echo NERD SCROLL
echo ============================================================
echo.
echo STEP 1 folder:
echo   %~dp01_DROP_TEXT_FILE_HERE
echo.
echo STEP 2:
echo   This launcher is running Nerd Scroll now.
echo.
echo Stop anytime with Ctrl+C.
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python "_nerd_scroll_app\start_nerd_scroll.py" --root "%~dp0" --drop-zone
    goto done
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py "_nerd_scroll_app\start_nerd_scroll.py" --root "%~dp0" --drop-zone
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
echo.
echo Nerd Scroll closed.
pause

@echo off
title Nerd Scroll - Drop Zone Legacy
cd /d "%~dp0"

echo Nerd Scroll Drop-Zone Legacy Mode
echo.
echo Drop a file into 1_DROP_TEXT_FILE_HERE, then this launcher types it.
echo.

python "_nerd_scroll_app\start_nerd_scroll.py" --root . --drop-zone

echo.
echo Nerd Scroll closed.
pause

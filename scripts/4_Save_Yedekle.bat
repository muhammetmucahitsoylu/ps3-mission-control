@echo off
setlocal
cd /d "%~dp0..\"
title PS3 Save Game Yedekleme Yoneticisi
color 0D
echo ================================================================
echo   PS3 SAVE GAME YEDEKLEME YONET?C?S?
echo ================================================================
echo.

py tools\save_manager.py
if errorlevel 1 (
    python tools\save_manager.py
)
echo.
pause

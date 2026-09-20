@echo off
setlocal
cd /d "%~dp0..\"
title PS3 Etkilesimli Oyun Baslatici
color 0E
echo ================================================================
echo   PS3 ETK?LES?ML? OYUN BASLAT?C?
echo ================================================================
echo.

py tools\game_launcher.py
if errorlevel 1 (
    python tools\game_launcher.py
)
echo.
pause

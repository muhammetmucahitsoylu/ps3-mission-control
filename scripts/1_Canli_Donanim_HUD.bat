@echo off
setlocal
cd /d "%~dp0..\"
title PS3 Canli Donanim Telemetri HUD
color 0A
echo ================================================================
echo   PS3 CANL? DONAN?M TELEMETR? HUD
echo ================================================================
echo.

py tools\live_hud.py
if errorlevel 1 (
    python tools\live_hud.py
)
echo.
pause

@echo off
setlocal
cd /d "%~dp0..\"
title PS3 Ghost Sentinel Termal Nobetci
color 0A
echo ================================================================
echo   PS3 GHOST SENT?NEL TERMAL NOBETC?
echo ================================================================
echo.

py tools\ghost_sentinel.py
if errorlevel 1 (
    python tools\ghost_sentinel.py
)
echo.
pause

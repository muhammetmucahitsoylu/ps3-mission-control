@echo off
setlocal
cd /d "%~dp0"
title PS3 Acimasiz Donanim ve HDD Test Kiti
color 0F
echo ================================================================
echo   PS3 AC?MAS?Z DONAN?M VE HDD TEST K?T?
echo ================================================================
echo.

py tools\hardware_audit.py
if errorlevel 1 (
    python tools\hardware_audit.py
)
echo.
pause

@echo off
setlocal
cd /d "%~dp0"
title PS3 Sistem ve Onbellek Temizleyici
color 0C
echo ================================================================
echo   PS3 S?STEM VE ONBELLEK TEM?ZLEY?C?
echo ================================================================
echo.

py tools\system_cleaner.py
if errorlevel 1 (
    python tools\system_cleaner.py
)
echo.
pause

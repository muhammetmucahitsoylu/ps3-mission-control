@echo off
setlocal
cd /d "%~dp0"
title PS3 Cyberpunk Web Kokpiti
color 0B
echo ================================================================
echo   PS3 CYBERPUNK WEB KOKP?T?
echo ================================================================
echo.
start http://localhost:8080
py tools\web_cockpit.py
if errorlevel 1 (
    python tools\web_cockpit.py
)
echo.
pause

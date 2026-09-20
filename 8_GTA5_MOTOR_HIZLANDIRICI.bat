@echo off
setlocal
cd /d "%~dp0"
title GTA 5 RAGE Motor ve Streaming Hizlandirici
color 0E
echo ================================================================
echo   GTA 5 RAGE MOTOR VE STREAM?NG H?ZLAND?R?C?
echo ================================================================
echo.

py tools\gta5_optimizer.py
if errorlevel 1 (
    python tools\gta5_optimizer.py
)
echo.
pause

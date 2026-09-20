@echo off
setlocal
cd /d "%~dp0"
title PS3 Derin VSH RAM Hizlandirici
color 0B
echo ================================================================
echo   PS3 DER?N VSH RAM H?ZLAND?R?C?
echo ================================================================
echo.

py tools\ram_booster.py
if errorlevel 1 (
    python tools\ram_booster.py
)
echo.
pause

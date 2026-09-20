@echo off
setlocal
cd /d "%~dp0"
title PS3 Blu-Ray Hayalet Dolgu Analizoru
color 0D
echo ================================================================
echo   PS3 BLU-RAY HAYALET DOLGU ANAL?ZORU
echo ================================================================
echo.

py tools\phantom_trimmer.py
if errorlevel 1 (
    python tools\phantom_trimmer.py
)
echo.
pause

@echo off
REM Get the directory of the current script
set current_dir=%~dp0

REM Change to the script's directory
cd /d %current_dir%

REM Run the Python script
python gui.py

pause

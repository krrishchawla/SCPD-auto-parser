@echo off
setlocal

REM Determine the directory where the script is located
set current_dir=%~dp0

REM Run the Python script
python "%current_dir%gui.py"

endlocal

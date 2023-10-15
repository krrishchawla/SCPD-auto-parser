@echo off

setlocal

set "current_dir=%~dp0"

python "%current_dir%process.py"

endlocal

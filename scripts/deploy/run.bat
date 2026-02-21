@echo off
setlocal
:: Get the directory where the script is located (scripts\deploy)
set "SCRIPT_DIR=%~dp0"
:: Move two levels up to reach project root
set "ROOT_DIR=%SCRIPT_DIR%..\..\"
cd /d "%ROOT_DIR%"

:: Ensure logs directory exists
if not exist "logs" mkdir "logs"

echo Starting application...
:: Run application and log output to logs\startup_log.txt
python -m uv run start >> logs\startup_log.txt 2>&1
endlocal
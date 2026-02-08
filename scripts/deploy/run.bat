@echo off
cd /d "C:\Users\pgugnowski\deployed\suwalski-assistant"
python -m uv run start >> startup_log.txt 2>&1
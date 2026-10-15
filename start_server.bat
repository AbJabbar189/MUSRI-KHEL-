@echo off
title Misri Khel Qaumi Ittehad Server
echo Starting Misri Khel Digital Platform Server...
cd /d "%~dp0"
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
pause

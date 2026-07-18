@echo off
cd /d "%~dp0"
"D:\Anaconda3\envs\YOLO\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8010 --reload
pause

@echo off
title LinkedIn AI Engagement Agent
cd /d C:\Users\manis\linkedin-agent

echo ============================================
echo   LinkedIn AI Engagement Agent
echo ============================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
python main.py

echo.
echo ============================================
echo Agent stopped.
echo ============================================
pause

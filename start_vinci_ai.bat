@echo off
title Vinci AI Startup
echo =====================================
echo   STARTING VINCI AI SYSTEM
echo =====================================
echo.

:: Resolve project root from this batch file's location
set "PROJECT_DIR=%~dp0"

:: Step 1 — Start Ollama in background
echo Starting Ollama...
start "" /min cmd /c "ollama serve"
timeout /t 3 >nul

:: Step 2 — Start FastAPI backend
echo Starting FastAPI backend...
start "" cmd /c "cd /d "%PROJECT_DIR%" && uvicorn backend.server:app --reload"
timeout /t 3 >nul

:: Step 3 — Open the Vinci Chat UI
echo Opening Vinci Chat Interface...
start "" "%PROJECT_DIR%frontend\index.html"

echo.
echo Vinci AI started successfully!
echo Close this window anytime.
pause

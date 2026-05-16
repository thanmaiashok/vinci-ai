@echo off
title Stop Vinci AI
echo =====================================
echo   STOPPING VINCI AI SYSTEM
echo =====================================
echo.

echo Killing FastAPI...
taskkill /F /IM python.exe >nul 2>&1

echo Killing Ollama...
taskkill /F /IM ollama.exe >nul 2>&1

echo All services stopped.
pause
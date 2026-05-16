@echo off
title Vinci AI — Setup
echo.
echo ╔══════════════════════════════════════════╗
echo ║         VINCI AI — SETUP WIZARD          ║
echo ╚══════════════════════════════════════════╝
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

:: ── Step 1: Check Python ─────────────────────────────
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  ERROR: Python not found.
    echo  Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)
python --version
echo  OK.
echo.

:: ── Step 2: Create virtual environment ───────────────
echo [2/5] Creating virtual environment...
if exist "venv\" (
    echo  Virtual environment already exists. Skipping.
) else (
    python -m venv venv
    echo  Created: venv\
)
echo.

:: ── Step 3: Install dependencies ─────────────────────
echo [3/5] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo  ERROR: pip install failed. Check requirements.txt.
    pause
    exit /b 1
)
echo  Dependencies installed.
echo.

:: ── Step 4: Check Ollama ─────────────────────────────
echo [4/5] Checking Ollama...
ollama --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  WARNING: Ollama not found in PATH.
    echo  Download from: https://ollama.com/download
    echo  After installing, run: ollama pull llama3.1:8b-instruct-q4_K_M
    echo  Then re-run this setup.
    pause
    exit /b 1
)
echo  Ollama found. Pulling LLM model (this may take a while)...
ollama pull llama3.1:8b-instruct-q4_K_M
echo  Model ready.
echo.

:: ── Step 5: Build FAISS vector index ─────────────────
echo [5/5] Building FAISS vector index from knowledge base...
if exist "data\vinci_index.faiss" (
    echo  Index already exists. Skipping rebuild.
    echo  To force rebuild, delete data\vinci_index.faiss and re-run setup.
) else (
    python -m rag.build_index
    if %ERRORLEVEL% NEQ 0 (
        echo  ERROR: Index build failed. Check data\vinci_labeled.jsonl exists.
        pause
        exit /b 1
    )
    echo  FAISS index built successfully.
)
echo.

:: ── Done ─────────────────────────────────────────────
echo ╔══════════════════════════════════════════╗
echo ║         SETUP COMPLETE!                  ║
echo ║                                          ║
echo ║  Run:  start_vinci_ai.bat                ║
echo ║  Then open: http://localhost:8000        ║
echo ╚══════════════════════════════════════════╝
echo.
pause

@echo off
title Mugil Soft Solutions - AI Co-Founder Agent
color 0B

:: ============================================================
::  Mugil AI Co-Founder — Quick Launch Script
::  Double-click to run. No Python knowledge required.
:: ============================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ── Locate venv Python ───────────────────────────────────────
set "PYTHON=.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
    echo.
    echo  [ERROR] Virtual environment not found at .venv\
    echo  Please run setup first:
    echo    python -m venv .venv
    echo    .venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:: ── Check .env exists ────────────────────────────────────────
if not exist ".env" (
    echo.
    echo  [WARNING] .env file not found. Copying from .env.example ...
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo  .env created. Please edit it and add your GEMINI_API_KEY.
    ) else (
        echo  [ERROR] .env.example also missing. Cannot continue.
    )
    echo.
    pause
    exit /b 1
)

:MENU
cls
echo.
echo  +=======================================================+
echo  ^|      MUGIL SOFT SOLUTIONS - AI CO-FOUNDER AGENT      ^|
echo  ^|       Innovating Today. Empowering Tomorrow.          ^|
echo  +=======================================================+
echo.
echo   [1]  Launch Web App          (browser UI on http://127.0.0.1:8000)
echo   [2]  Launch Web App (LAN)    (share on Wi-Fi / phone access)
echo   [3]  Interactive Chat        (terminal chat session)
echo   [4]  Ask a Question          (single question, quick answer)
echo   [5]  Governance Audit        (risk tier check for a project)
echo   [6]  Knowledge Base Status   (indexed docs summary)
echo   [7]  List Agent Personas     (all available AI agents)
echo   [8]  Run Tests               (verify everything is working)
echo   [9]  Install / Update Deps   (pip install -r requirements.txt)
echo   [0]  Exit
echo.
set /p CHOICE="  Enter your choice (0-9): "

if "%CHOICE%"=="1" goto WEB_LOCAL
if "%CHOICE%"=="2" goto WEB_LAN
if "%CHOICE%"=="3" goto CHAT
if "%CHOICE%"=="4" goto ASK
if "%CHOICE%"=="5" goto AUDIT
if "%CHOICE%"=="6" goto STATUS
if "%CHOICE%"=="7" goto AGENTS
if "%CHOICE%"=="8" goto TESTS
if "%CHOICE%"=="9" goto INSTALL
if "%CHOICE%"=="0" goto EXIT

echo  [Invalid choice] Please enter a number from 0 to 9.
timeout /t 2 >nul
goto MENU


:WEB_LOCAL
cls
echo.
echo  Starting Web App on http://127.0.0.1:8000 ...
echo  Press Ctrl+C to stop the server.
echo.
"%PYTHON%" run_web.py --host 127.0.0.1 --port 8000
goto AFTER_RUN


:WEB_LAN
cls
echo.
echo  Starting Web App with LAN access (Wi-Fi sharing enabled) ...
echo  Other devices on your network can connect using your PC's IP.
echo  Press Ctrl+C to stop the server.
echo.
"%PYTHON%" run_web.py --host 0.0.0.0 --port 8000
goto AFTER_RUN


:CHAT
cls
echo.
echo  Starting interactive chat session ...
echo  Type your question and press Enter. Type 'exit' to quit.
echo  Action commands: !email  !write  !delete  !run
echo.
"%PYTHON%" cli.py chat
goto AFTER_RUN


:ASK
cls
echo.
set /p QUESTION="  Enter your question: "
if "!QUESTION!"=="" (
    echo  [No question entered]
    timeout /t 2 >nul
    goto MENU
)
echo.
"%PYTHON%" cli.py ask "!QUESTION!"
goto AFTER_RUN


:AUDIT
cls
echo.
set /p DESC="  Describe the project/action to audit (e.g. 'medical AI diagnosis tool'): "
if "!DESC!"=="" (
    echo  [No description entered]
    timeout /t 2 >nul
    goto MENU
)
echo.
"%PYTHON%" cli.py audit --desc "!DESC!"
goto AFTER_RUN


:STATUS
cls
echo.
"%PYTHON%" cli.py status
goto AFTER_RUN


:AGENTS
cls
echo.
"%PYTHON%" cli.py agents
goto AFTER_RUN


:TESTS
cls
echo.
echo  Running test suite ...
echo.
"%PYTHON%" -m pytest tests/ -v --tb=short 2>&1
goto AFTER_RUN


:INSTALL
cls
echo.
echo  Installing / updating dependencies from requirements.txt ...
echo.
"%PYTHON%" -m pip install -r requirements.txt
echo.
echo  Done. Press any key to return to menu.
pause >nul
goto MENU


:AFTER_RUN
echo.
echo  -------------------------------------------------------
echo  Press any key to return to the menu, or close to exit.
echo  -------------------------------------------------------
pause >nul
goto MENU


:EXIT
cls
echo.
echo  Goodbye! Mugil AI Co-Founder signing off.
echo.
exit /b 0

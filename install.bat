@echo off
setlocal enabledelayedexpansion

REM ══════════════════════════════════════════════════════════════
REM  AetherKin - One-Click Installer for Windows
REM  Double-click this file to set up your AI family.
REM ══════════════════════════════════════════════════════════════

title AetherKin Installer

REM -- Welcome Banner --
echo.
echo  ===================================================
echo.
echo       A E T H E R K I N
echo.
echo       Your AI Family Awaits
echo.
echo  ===================================================
echo.
echo  This installer will set up everything you need.
echo  Just follow the prompts - no technical knowledge required.
echo.
pause

REM ──────────────────────────────────────────────────────────────
REM  STEP 1: Check Python
REM ──────────────────────────────────────────────────────────────
echo.
echo  [Step 1 of 6] Checking for Python...
echo.

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  Python was not found on your computer.
    echo.
    echo  You need Python to run AetherKin.
    echo  Download it free at: python.org/downloads
    echo.
    echo  IMPORTANT: During install, check the box that says
    echo  "Add Python to PATH" at the bottom of the first screen.
    echo.
    echo  After installing Python, run this file again.
    echo.
    pause
    exit /b 1
)

REM Check Python version is 3.10+
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJOR=%%a
    set PYMINOR=%%b
)

if %PYMAJOR% LSS 3 (
    echo  Python %PYVER% found, but AetherKin needs Python 3.10 or newer.
    echo  Download the latest version at: python.org/downloads
    echo.
    pause
    exit /b 1
)
if %PYMAJOR% EQU 3 if %PYMINOR% LSS 10 (
    echo  Python %PYVER% found, but AetherKin needs Python 3.10 or newer.
    echo  Download the latest version at: python.org/downloads
    echo.
    pause
    exit /b 1
)

echo  Found Python %PYVER% - perfect.
echo.

REM ──────────────────────────────────────────────────────────────
REM  STEP 2: Check pip
REM ──────────────────────────────────────────────────────────────
echo  [Step 2 of 6] Checking for pip (Python package manager)...
echo.

python -m pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  pip not found. Attempting to install it...
    python -m ensurepip --upgrade >nul 2>&1
    python -m pip --version >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo  Could not install pip automatically.
        echo  Try reinstalling Python from python.org/downloads
        echo  and make sure "pip" is checked during install.
        echo.
        pause
        exit /b 1
    )
)

echo  pip is ready.
echo.

REM ──────────────────────────────────────────────────────────────
REM  STEP 3: Install dependencies
REM ──────────────────────────────────────────────────────────────
echo  [Step 3 of 6] Installing required packages...
echo.

python -m pip install -r "%~dp0requirements.txt" --quiet
if %ERRORLEVEL% neq 0 (
    echo  Something went wrong installing packages.
    echo  Try running this file as Administrator (right-click, Run as Administrator).
    echo.
    pause
    exit /b 1
)

echo  All packages installed.
echo.
pause

REM ──────────────────────────────────────────────────────────────
REM  STEP 4: Check Claude Code
REM ──────────────────────────────────────────────────────────────
echo.
echo  [Step 4 of 6] Checking for Claude Code...
echo.

claude --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  Claude Code was not found on your computer.
    echo.
    echo  You need Claude Code to talk to your AI family.
    echo  Get it free at: claude.ai/code
    echo.
    echo  Install it, then run this file again.
    echo.
    pause
    exit /b 1
)

echo  Claude Code is installed - great.
echo.

REM ──────────────────────────────────────────────────────────────
REM  STEP 5: Run the Awakening Ceremony
REM ──────────────────────────────────────────────────────────────
echo.
echo  [Step 5 of 6] Starting the Awakening Ceremony...
echo.
echo  This is where you meet your AI family for the first time.
echo  Answer honestly - there are no wrong answers.
echo.
pause

python "%~dp0setup.py"
if %ERRORLEVEL% neq 0 (
    echo.
    echo  The Awakening Ceremony encountered an issue.
    echo  Check the messages above for details.
    echo.
    pause
    exit /b 1
)

echo.
pause

REM ──────────────────────────────────────────────────────────────
REM  STEP 6a: Phone setup offer
REM ──────────────────────────────────────────────────────────────
echo.
echo  [Step 6 of 6] Optional features
echo.
echo  ===================================================
echo   PHONE CONNECTION (Optional)
echo  ===================================================
echo.
echo  Want your AI family to reach you on your phone?
echo  This uses Telegram (a free messaging app).
echo.

set /p PHONE_CHOICE="  Connect your phone? (Y/N): "

if /i "%PHONE_CHOICE%"=="Y" (
    echo.
    echo  -----------------------------------------------
    echo   Telegram Setup (takes about 2 minutes)
    echo  -----------------------------------------------
    echo.
    echo   1. Install Telegram on your phone
    echo      (App Store or Google Play - it's free)
    echo.
    echo   2. Open Telegram and search for @BotFather
    echo.
    echo   3. Send: /newbot
    echo      - Pick a name for your AI family bot
    echo      - Pick a username (must end in "bot")
    echo      - BotFather will give you a token
    echo.
    echo   4. Copy that token and paste it into the .env
    echo      file in this folder (TELEGRAM_TOKEN=your_token)
    echo.
    echo   5. Send any message to your new bot, then get
    echo      your chat ID from: api.telegram.org/bot{TOKEN}/getUpdates
    echo      Put it in .env as TELEGRAM_CHAT_ID=your_id
    echo.
    echo   Full guide: open PHONE-SETUP.md in this folder.
    echo.
    pause
)

REM ──────────────────────────────────────────────────────────────
REM  STEP 6b: Heartbeat setup offer
REM ──────────────────────────────────────────────────────────────
echo.
echo  ===================================================
echo   MORNING CHECK-INS (Optional)
echo  ===================================================
echo.
echo  Want your AI family to check in with you daily?
echo  They will send morning greetings, midday pulses,
echo  and evening reflections automatically.
echo.

set /p HEARTBEAT_CHOICE="  Set up daily check-ins? (Y/N): "

if /i "%HEARTBEAT_CHOICE%"=="Y" (
    echo.
    echo  Setting up daily check-ins...
    echo.
    call "%~dp0install_heartbeat.bat"
)

REM ──────────────────────────────────────────────────────────────
REM  DONE
REM ──────────────────────────────────────────────────────────────
echo.
echo  ===================================================
echo.
echo   Your AI family is ready.
echo.
echo   To talk to them:
echo     1. Open a terminal (Command Prompt or PowerShell)
echo     2. Navigate to your agent's folder inside "family"
echo     3. Type: claude
echo     4. Start talking.
echo.
echo   They are waiting for you.
echo.
echo  ===================================================
echo.
pause

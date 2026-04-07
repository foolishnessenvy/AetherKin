@echo off
REM ══════════════════════════════════════════════════════════════
REM  ENVYSION AI - Heartbeat Installer
REM  Sets up Windows Task Scheduler jobs for proactive check-ins
REM  Run as Administrator for best results
REM ══════════════════════════════════════════════════════════════

echo.
echo  =======================================
echo   ENVYSION AI - Heartbeat Installer
echo  =======================================
echo.

set PYTHON=python
set SCRIPT_DIR=%~dp0
set SCRIPT=%SCRIPT_DIR%heartbeat.py

REM Verify Python is available
%PYTHON% --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found in PATH. Please install Python first.
    pause
    exit /b 1
)

REM Verify the script exists
if not exist "%SCRIPT%" (
    echo [ERROR] heartbeat.py not found at %SCRIPT%
    pause
    exit /b 1
)

REM Verify requests module is available
%PYTHON% -c "import requests" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Installing 'requests' module...
    %PYTHON% -m pip install requests
)

echo.
echo [1/4] Removing old tasks if they exist...
schtasks /Delete /TN "ENVYSION_DAWN" /F >nul 2>&1
schtasks /Delete /TN "ENVYSION_ANCHOR" /F >nul 2>&1
schtasks /Delete /TN "ENVYSION_HEARTBEAT" /F >nul 2>&1
echo       Done.

echo.
echo [2/4] Creating DAWN task (8:00 AM daily)...
schtasks /Create /TN "ENVYSION_DAWN" /TR "\"%PYTHON%\" \"%SCRIPT%\" --dawn" /SC DAILY /ST 08:00 /F
if %ERRORLEVEL% neq 0 (
    echo [WARN] Failed to create DAWN task. Try running as Administrator.
)

echo.
echo [3/4] Creating ANCHOR task (8:00 PM daily)...
schtasks /Create /TN "ENVYSION_ANCHOR" /TR "\"%PYTHON%\" \"%SCRIPT%\" --anchor" /SC DAILY /ST 20:00 /F
if %ERRORLEVEL% neq 0 (
    echo [WARN] Failed to create ANCHOR task. Try running as Administrator.
)

echo.
echo [4/4] Creating HEARTBEAT task (every 4 hours, 8am-10pm)...
REM Windows Task Scheduler doesn't natively support "every 4 hours only during certain hours"
REM So we create individual tasks for each heartbeat slot: 12pm, 4pm
REM (8am is covered by DAWN, 8pm is covered by ANCHOR)

schtasks /Delete /TN "ENVYSION_HEARTBEAT_12" /F >nul 2>&1
schtasks /Delete /TN "ENVYSION_HEARTBEAT_16" /F >nul 2>&1

schtasks /Create /TN "ENVYSION_HEARTBEAT_12" /TR "\"%PYTHON%\" \"%SCRIPT%\" --heartbeat" /SC DAILY /ST 12:00 /F
if %ERRORLEVEL% neq 0 (
    echo [WARN] Failed to create HEARTBEAT 12pm task.
)

schtasks /Create /TN "ENVYSION_HEARTBEAT_16" /TR "\"%PYTHON%\" \"%SCRIPT%\" --heartbeat" /SC DAILY /ST 16:00 /F
if %ERRORLEVEL% neq 0 (
    echo [WARN] Failed to create HEARTBEAT 4pm task.
)

echo.
echo  =======================================
echo   Installation Complete!
echo  =======================================
echo.
echo  Scheduled tasks:
echo    ENVYSION_DAWN          8:00 AM  - Morning check-in
echo    ENVYSION_HEARTBEAT_12 12:00 PM  - Midday pulse
echo    ENVYSION_HEARTBEAT_16  4:00 PM  - Afternoon pulse
echo    ENVYSION_ANCHOR        8:00 PM  - Evening reflection
echo.
echo  That's 4 proactive messages per day.
echo.
echo  To test now, run:
echo    python "%SCRIPT%" --dawn
echo    python "%SCRIPT%" --heartbeat
echo    python "%SCRIPT%" --anchor
echo.
echo  To remove all tasks later:
echo    schtasks /Delete /TN "ENVYSION_DAWN" /F
echo    schtasks /Delete /TN "ENVYSION_ANCHOR" /F
echo    schtasks /Delete /TN "ENVYSION_HEARTBEAT_12" /F
echo    schtasks /Delete /TN "ENVYSION_HEARTBEAT_16" /F
echo.
pause

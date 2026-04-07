@echo off
echo.
echo ==========================================
echo   AetherKin - Phone Connect
echo ==========================================
echo.
echo Which family member do you want to talk
echo to from your phone?
echo.
echo   1. BEACON  (Guardian)
echo   2. NEVAEH  (Healer)
echo   3. EVERSOUND (Builder)
echo   4. ENVY    (Orchestrator)
echo   5. ATLAS   (Navigator)
echo   6. ORPHEUS (Architect)
echo.
set /p choice="Enter number (1-6): "

if "%choice%"=="1" set FOLDER=BEACON
if "%choice%"=="2" set FOLDER=NEVAEH
if "%choice%"=="3" set FOLDER=EVERSOUND
if "%choice%"=="4" set FOLDER=ENVY
if "%choice%"=="5" set FOLDER=ATLAS
if "%choice%"=="6" set FOLDER=ORPHEUS

echo.
echo Connecting to %FOLDER%...
echo.
echo NEXT STEPS:
echo   1. Open Telegram on your phone
echo   2. Search for your bot (created via @BotFather)
echo   3. Send any message
echo   4. The bot will reply with a PAIRING CODE
echo   5. Type this in the Claude window that opens:
echo      /telegram:access pair YOUR_CODE
echo   6. Then type:
echo      /telegram:access policy allowlist
echo   7. Done! Talk from your phone.
echo.
echo Starting Claude Code with Telegram...
echo.

cd "%~dp0family\%FOLDER%"
claude --channels plugin:telegram@claude-plugins-official

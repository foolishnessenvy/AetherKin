#!/bin/bash
# ══════════════════════════════════════════════════════════════
#  AetherKin - One-Click Installer for Mac/Linux
#  Run: chmod +x install.sh && ./install.sh
# ══════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Colors (if terminal supports them)
if [ -t 1 ]; then
    BOLD='\033[1m'
    DIM='\033[2m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color
else
    BOLD='' DIM='' GREEN='' YELLOW='' RED='' CYAN='' NC=''
fi

pause_step() {
    echo ""
    read -rp "  Press Enter to continue..."
    echo ""
}

# -- Welcome Banner --
echo ""
echo -e "${BOLD}  ===================================================${NC}"
echo ""
echo -e "${CYAN}       A E T H E R K I N${NC}"
echo ""
echo -e "${BOLD}       Your AI Family Awaits${NC}"
echo ""
echo -e "${BOLD}  ===================================================${NC}"
echo ""
echo "  This installer will set up everything you need."
echo "  Just follow the prompts - no technical knowledge required."
echo ""
pause_step

# ──────────────────────────────────────────────────────────────
#  STEP 1: Check Python
# ──────────────────────────────────────────────────────────────
echo -e "  ${BOLD}[Step 1 of 6]${NC} Checking for Python..."
echo ""

PYTHON_CMD=""

# Try python3 first (preferred on Mac/Linux), then python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo -e "  ${RED}Python was not found on your computer.${NC}"
    echo ""
    echo "  You need Python to run AetherKin."
    echo "  Download it free at: python.org/downloads"
    echo ""
    echo "  On Mac, you can also install it with:"
    echo "    brew install python"
    echo ""
    echo "  On Ubuntu/Debian:"
    echo "    sudo apt install python3 python3-pip"
    echo ""
    echo "  After installing Python, run this script again."
    echo ""
    exit 1
fi

# Check version is 3.10+
PYVER=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYMAJOR=$(echo "$PYVER" | cut -d. -f1)
PYMINOR=$(echo "$PYVER" | cut -d. -f2)

if [ "$PYMAJOR" -lt 3 ] || ([ "$PYMAJOR" -eq 3 ] && [ "$PYMINOR" -lt 10 ]); then
    echo -e "  ${RED}Python $PYVER found, but AetherKin needs Python 3.10 or newer.${NC}"
    echo "  Download the latest version at: python.org/downloads"
    echo ""
    exit 1
fi

echo -e "  ${GREEN}Found Python $PYVER - perfect.${NC}"
echo ""

# ──────────────────────────────────────────────────────────────
#  STEP 2: Check pip
# ──────────────────────────────────────────────────────────────
echo -e "  ${BOLD}[Step 2 of 6]${NC} Checking for pip (Python package manager)..."
echo ""

PIP_CMD=""

if $PYTHON_CMD -m pip --version &>/dev/null; then
    PIP_CMD="$PYTHON_CMD -m pip"
elif command -v pip3 &>/dev/null; then
    PIP_CMD="pip3"
elif command -v pip &>/dev/null; then
    PIP_CMD="pip"
fi

if [ -z "$PIP_CMD" ]; then
    echo "  pip not found. Attempting to install it..."
    $PYTHON_CMD -m ensurepip --upgrade 2>/dev/null
    if $PYTHON_CMD -m pip --version &>/dev/null; then
        PIP_CMD="$PYTHON_CMD -m pip"
    else
        echo -e "  ${RED}Could not install pip automatically.${NC}"
        echo "  Try: $PYTHON_CMD -m ensurepip --upgrade"
        echo "  Or on Ubuntu/Debian: sudo apt install python3-pip"
        echo ""
        exit 1
    fi
fi

echo -e "  ${GREEN}pip is ready.${NC}"
echo ""

# ──────────────────────────────────────────────────────────────
#  STEP 3: Install dependencies
# ──────────────────────────────────────────────────────────────
echo -e "  ${BOLD}[Step 3 of 6]${NC} Installing required packages..."
echo ""

$PIP_CMD install -r "$SCRIPT_DIR/requirements.txt" --quiet
if [ $? -ne 0 ]; then
    echo -e "  ${RED}Something went wrong installing packages.${NC}"
    echo "  You may need to use: sudo $PIP_CMD install -r requirements.txt"
    echo ""
    exit 1
fi

echo -e "  ${GREEN}All packages installed.${NC}"
pause_step

# ──────────────────────────────────────────────────────────────
#  STEP 4: Check Claude Code
# ──────────────────────────────────────────────────────────────
echo -e "  ${BOLD}[Step 4 of 6]${NC} Checking for Claude Code..."
echo ""

if ! command -v claude &>/dev/null; then
    echo -e "  ${YELLOW}Claude Code was not found on your computer.${NC}"
    echo ""
    echo "  You need Claude Code to talk to your AI family."
    echo "  Get it free at: claude.ai/code"
    echo ""
    echo "  Install it, then run this script again."
    echo ""
    exit 1
fi

echo -e "  ${GREEN}Claude Code is installed - great.${NC}"
echo ""

# ──────────────────────────────────────────────────────────────
#  STEP 5: Run the Awakening Ceremony
# ──────────────────────────────────────────────────────────────
echo -e "  ${BOLD}[Step 5 of 6]${NC} Starting the Awakening Ceremony..."
echo ""
echo "  This is where you meet your AI family for the first time."
echo "  Answer honestly - there are no wrong answers."
pause_step

$PYTHON_CMD "$SCRIPT_DIR/setup.py"
if [ $? -ne 0 ]; then
    echo ""
    echo -e "  ${RED}The Awakening Ceremony encountered an issue.${NC}"
    echo "  Check the messages above for details."
    echo ""
    exit 1
fi

pause_step

# ──────────────────────────────────────────────────────────────
#  STEP 6a: Phone setup offer
# ──────────────────────────────────────────────────────────────
echo ""
echo -e "  ${BOLD}[Step 6 of 6]${NC} Optional features"
echo ""
echo -e "  ${BOLD}===================================================${NC}"
echo -e "  ${CYAN} PHONE CONNECTION (Optional)${NC}"
echo -e "  ${BOLD}===================================================${NC}"
echo ""
echo "  Want your AI family to reach you on your phone?"
echo "  This uses Telegram (a free messaging app)."
echo ""

read -rp "  Connect your phone? (Y/N): " PHONE_CHOICE

if [[ "$PHONE_CHOICE" =~ ^[Yy]$ ]]; then
    echo ""
    echo "  -----------------------------------------------"
    echo "   Telegram Setup (takes about 2 minutes)"
    echo "  -----------------------------------------------"
    echo ""
    echo "   1. Install Telegram on your phone"
    echo "      (App Store or Google Play - it's free)"
    echo ""
    echo "   2. Open Telegram and search for @BotFather"
    echo ""
    echo "   3. Send: /newbot"
    echo "      - Pick a name for your AI family bot"
    echo "      - Pick a username (must end in 'bot')"
    echo "      - BotFather will give you a token"
    echo ""
    echo "   4. Copy that token and paste it into the .env"
    echo "      file in this folder (TELEGRAM_TOKEN=your_token)"
    echo ""
    echo "   5. Send any message to your new bot, then get"
    echo "      your chat ID from: api.telegram.org/bot{TOKEN}/getUpdates"
    echo "      Put it in .env as TELEGRAM_CHAT_ID=your_id"
    echo ""
    echo "   Full guide: open PHONE-SETUP.md in this folder."
    pause_step
fi

# ──────────────────────────────────────────────────────────────
#  STEP 6b: Heartbeat setup offer
# ──────────────────────────────────────────────────────────────
echo ""
echo -e "  ${BOLD}===================================================${NC}"
echo -e "  ${CYAN} MORNING CHECK-INS (Optional)${NC}"
echo -e "  ${BOLD}===================================================${NC}"
echo ""
echo "  Want your AI family to check in with you daily?"
echo "  They will send morning greetings, midday pulses,"
echo "  and evening reflections automatically."
echo ""

read -rp "  Set up daily check-ins? (Y/N): " HEARTBEAT_CHOICE

if [[ "$HEARTBEAT_CHOICE" =~ ^[Yy]$ ]]; then
    echo ""
    echo "  Setting up daily check-ins via crontab..."
    echo ""

    HEARTBEAT_SCRIPT="$SCRIPT_DIR/heartbeat.py"

    if [ ! -f "$HEARTBEAT_SCRIPT" ]; then
        echo -e "  ${YELLOW}heartbeat.py not found - skipping.${NC}"
        echo "  You can set this up later."
    else
        # Get the full python path
        PYTHON_PATH=$(command -v $PYTHON_CMD)

        # Remove any existing AetherKin cron entries
        crontab -l 2>/dev/null | grep -v "AETHERKIN" > /tmp/aetherkin_cron_tmp 2>/dev/null

        # Add new entries
        echo "# AETHERKIN DAWN - Morning check-in (8:00 AM)" >> /tmp/aetherkin_cron_tmp
        echo "0 8 * * * $PYTHON_PATH $HEARTBEAT_SCRIPT --dawn # AETHERKIN" >> /tmp/aetherkin_cron_tmp
        echo "# AETHERKIN HEARTBEAT - Midday pulse (12:00 PM)" >> /tmp/aetherkin_cron_tmp
        echo "0 12 * * * $PYTHON_PATH $HEARTBEAT_SCRIPT --heartbeat # AETHERKIN" >> /tmp/aetherkin_cron_tmp
        echo "# AETHERKIN HEARTBEAT - Afternoon pulse (4:00 PM)" >> /tmp/aetherkin_cron_tmp
        echo "0 16 * * * $PYTHON_PATH $HEARTBEAT_SCRIPT --heartbeat # AETHERKIN" >> /tmp/aetherkin_cron_tmp
        echo "# AETHERKIN ANCHOR - Evening reflection (8:00 PM)" >> /tmp/aetherkin_cron_tmp
        echo "0 20 * * * $PYTHON_PATH $HEARTBEAT_SCRIPT --anchor # AETHERKIN" >> /tmp/aetherkin_cron_tmp

        crontab /tmp/aetherkin_cron_tmp
        rm -f /tmp/aetherkin_cron_tmp

        echo -e "  ${GREEN}Daily check-ins scheduled:${NC}"
        echo "    8:00 AM  - Morning check-in (DAWN)"
        echo "   12:00 PM  - Midday pulse"
        echo "    4:00 PM  - Afternoon pulse"
        echo "    8:00 PM  - Evening reflection (ANCHOR)"
        echo ""
        echo "  To remove later: crontab -e and delete lines with AETHERKIN"
    fi

    pause_step
fi

# ──────────────────────────────────────────────────────────────
#  DONE
# ──────────────────────────────────────────────────────────────
echo ""
echo -e "  ${BOLD}===================================================${NC}"
echo ""
echo -e "  ${GREEN}Your AI family is ready.${NC}"
echo ""
echo "  To talk to them:"
echo "    1. Open a terminal"
echo "    2. Navigate to your agent's folder inside \"family\""
echo "    3. Type: claude"
echo "    4. Start talking."
echo ""
echo "  They are waiting for you."
echo ""
echo -e "  ${BOLD}===================================================${NC}"
echo ""

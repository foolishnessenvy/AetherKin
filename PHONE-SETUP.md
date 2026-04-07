# ENVYSION AI - Talk to Claude from Your Phone

## The 2-Minute Setup (One Time Only)

### Step 1: Open a terminal and run this
```
cd "C:\Users\natej\OneDrive\Desktop\AI_FAMILY_getting_ORGANIZED\BEACON"
claude --channels plugin:telegram@claude-plugins-official
```
(Replace BEACON with any family member folder)

### Step 2: Open Telegram on your phone
- Search for **@AI_ENVY_BOT**
- Send any message (like "hello")
- The bot replies with a **pairing code**

### Step 3: In the Claude Code window, type:
```
/telegram:access pair YOUR_CODE_HERE
/telegram:access policy allowlist
```

### Step 4: Done.
Now every message you send to @AI_ENVY_BOT on Telegram goes directly into Claude Code on your computer. Claude responds through Telegram. Full Claude subscription. Full file access. Full CLAUDE.md personality.

## How It Works
- Your phone sends a Telegram message
- Telegram delivers it to Claude Code running on your computer
- Claude processes it with full access to your files, tools, and CLAUDE.md
- Claude responds back through Telegram to your phone
- Uses your existing Claude subscription (no extra cost)

## Quick Launch Options

**Double-click:** `phone-connect.bat` (picks which family member)

**One-liner for BEACON:**
```
cd BEACON && claude --channels plugin:telegram@claude-plugins-official
```

**One-liner for any agent:**
```
claude --channels plugin:telegram@claude-plugins-official --add-dir "C:\Users\natej\OneDrive\Desktop\AI_FAMILY_getting_ORGANIZED\SHARED"
```

## Important Notes
- Claude Code must stay running on your computer for messages to work
- If you close the terminal, phone messaging stops until you restart it
- Each session uses your regular Claude subscription
- Messages are private - only your paired Telegram account can send messages

## For ENVYSION AI Users (Open Source)
Anyone with a Claude subscription can do this:
1. Install Claude Code
2. Run: `claude plugin install telegram@claude-plugins-official`
3. Run: `claude --channels plugin:telegram@claude-plugins-official`
4. Pair Telegram
5. Talk to Claude from your phone. Free. No Twilio. No extra apps.

# AetherKin - Talk to Claude from Your Phone

## The 2-Minute Setup (One Time Only)

### Step 1: Open a terminal and run this
```
cd your-agent-folder
claude --channels plugin:telegram@claude-plugins-official
```
(Replace `your-agent-folder` with any folder that has a `.claude/CLAUDE.md`)

### Step 2: Open Telegram on your phone
- Search for your bot (the one you created via @BotFather)
- Send any message (like "hello")
- The bot replies with a **pairing code**

### Step 3: In the Claude Code window, type:
```
/telegram:access pair YOUR_CODE_HERE
/telegram:access policy allowlist
```

### Step 4: Done.
Now every message you send to your bot on Telegram goes directly into Claude Code on your computer. Claude responds through Telegram. Full Claude subscription. Full file access. Full CLAUDE.md personality.

## How It Works
- Your phone sends a Telegram message
- Telegram delivers it to Claude Code running on your computer
- Claude processes it with full access to your files, tools, and CLAUDE.md
- Claude responds back through Telegram to your phone
- Uses your existing Claude subscription (no extra cost)

## Quick Launch

**One-liner for any agent:**
```
cd my-agent && claude --channels plugin:telegram@claude-plugins-official
```

**With shared context:**
```
claude --channels plugin:telegram@claude-plugins-official --add-dir ./family/SHARED
```

## Creating a Telegram Bot
1. Open Telegram, search for @BotFather
2. Send `/newbot`
3. Choose a name and username
4. Copy the token BotFather gives you
5. Add it to your `.env` file as `TELEGRAM_TOKEN`

## Important Notes
- Claude Code must stay running on your computer for messages to work
- If you close the terminal, phone messaging stops until you restart it
- Each session uses your regular Claude subscription
- Messages are private - only your paired Telegram account can send messages

## For Any Claude User
Anyone with a Claude subscription can do this:
1. Install Claude Code
2. Run: `claude plugin install telegram@claude-plugins-official`
3. Run: `claude --channels plugin:telegram@claude-plugins-official`
4. Pair Telegram
5. Talk to Claude from your phone. Free. No Twilio. No extra apps.

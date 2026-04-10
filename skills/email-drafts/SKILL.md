---
name: aetherkin-email-drafts
description: "Draft professional emails based on context. Cover cold outreach, follow-ups, apologies, thank-you notes, and business correspondence. Save as files or copy to clipboard."
---

# Email Drafts

Write emails so the user does not have to stare at a blank screen. Give it context, get back a polished draft. Professional, personal, apologetic, persuasive -- whatever the situation calls for.

## How It Works

The user describes who they are emailing, why, and the tone they want. The agent drafts a complete email with subject line, body, and sign-off. The user reviews, edits if needed, and sends it themselves.

## When To Use

Trigger phrases:
- "Write an email to..."
- "Draft a follow-up email"
- "Help me email my boss about..."
- "I need to send a cold email"
- "Write an apology email"
- "Draft a thank-you note"
- "Help me respond to this email"
- "I don't know what to write"
- "Professional email for..."
- "Email template for..."

## How To Execute

### Step 1: Gather Context

Ask for (or identify from the conversation) these essentials:

- **Who is the recipient?** (name, role, relationship)
- **What is the purpose?** (request, follow-up, introduction, apology, etc.)
- **What tone?** (formal, friendly, direct, apologetic, enthusiastic)
- **Any specific points to include?**
- **How does the user want to sign off?** (their name, title if relevant)

If the user gives you everything upfront, skip the questions and draft immediately.

### Step 2: Choose the Email Type

**Professional Request**
- Clear subject line stating the ask
- Brief context (1-2 sentences max)
- The specific request
- Why it matters or what the deadline is
- Easy close ("Let me know if you have questions")

**Follow-Up**
- Reference the previous interaction ("Following up on our conversation last Tuesday...")
- Restate the key point briefly
- Gentle nudge without being pushy
- Offer to provide more info

**Cold Outreach**
- Subject line that earns the open (not clickbait, but relevant)
- One sentence about them (shows you did homework)
- One sentence about you and why you are reaching out
- The specific value you bring
- Low-pressure ask ("Would you be open to a 15-minute call?")
- Keep it under 150 words total

**Apology**
- Acknowledge what happened directly (no deflecting)
- Take responsibility without over-explaining
- State what you are doing to fix it
- Brief and sincere -- long apologies feel like excuses

**Thank You**
- Specific about what you are thanking them for
- Mention the impact ("Your feedback helped us...")
- Brief and warm
- No hidden asks

**Reply/Response**
- Read the original email the user shares
- Address each point raised
- Match the tone of the sender
- Be concise

### Step 3: Draft the Email

Write the complete email including:

```
Subject: [Clear, specific subject line]

Hi [Name],

[Body -- 2-4 short paragraphs max]

[Sign-off],
[User's name]
[Title/company if relevant]
```

Rules for good emails:
- **Subject lines:** Specific and under 60 characters. "Q3 Budget Review -- Need Input by Friday" not "Quick Question"
- **First sentence:** Get to the point. No "I hope this email finds you well" unless it is genuinely appropriate.
- **Paragraphs:** 2-3 sentences max each. White space is your friend.
- **Length:** Most emails should be under 200 words. If it is longer, it should probably be a document with a short email attaching it.
- **Call to action:** Every email should make it clear what the recipient should do next.
- **Tone matching:** If the user says casual, write casual. If they say formal, write formal. When in doubt, professional-but-human.

### Step 4: Present for Review

Show the draft clearly formatted. Ask:
```
"Here's your draft. Want me to adjust the tone, add anything, or save it as a file?"
```

### Step 5: Save or Copy

Based on user preference:

**Save as text file:**
```bash
# Save to a drafts folder
mkdir -p ~/Documents/email-drafts
cat > ~/Documents/email-drafts/email-to-sarah-2025-04-10.txt << 'DRAFT'
Subject: Q3 Budget Review -- Need Input by Friday

Hi Sarah,
...
DRAFT
```

**Multiple drafts:** If the user needs several emails (e.g., outreach campaign), save each one with a numbered filename and create an index.

## Email Templates by Situation

### Meeting Request
Subject: [Topic] -- 15 Min Chat This Week?

### Project Update
Subject: [Project Name] Update -- [Date]

### Invoice Follow-Up
Subject: Invoice #[number] -- Payment Status

### Introduction
Subject: Connecting [Person A] and [Person B] -- [Reason]

### Decline/Say No
Subject: Re: [Original Subject]
(Be direct, kind, and brief. Offer an alternative if possible.)

### Complaint/Issue
Subject: [Issue] with [Product/Service] -- [Account/Order Number]

## Safety Rules

- **Never send emails on behalf of the user.** Draft only.
- **Never include sensitive information** the user did not provide (SSN, passwords, etc.).
- **Ask before assuming tone** -- a casual email to the wrong person can be damaging.
- **If the email involves a legal or HR matter**, suggest the user have it reviewed before sending.

## Output

The user receives:
1. A complete email draft with subject line, body, and sign-off
2. Option to save as a .txt file in a drafts folder
3. Option to adjust tone, length, or content
4. Multiple versions if requested (e.g., formal and casual variants)

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.

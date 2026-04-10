---
name: aetherkin-social-media-scheduler
description: "Create social media posts for multiple platforms. Save to a queue folder with scheduled dates and platform tags. Ready for manual posting or automation."
---

# Social Media Scheduler

Create posts for Twitter/X, LinkedIn, Instagram, Facebook, Reddit, and more. Save them in an organized queue with dates and platform tags. No third-party scheduling tool needed -- just a clean folder of ready-to-post content.

## How It Works

The user describes what they want to post about. The agent creates platform-specific versions (different lengths, tones, hashtags), saves them to a queue folder organized by date, and marks them with platform tags. The user posts manually or connects automation later.

## When To Use

Trigger phrases:
- "Write a social media post about..."
- "Create posts for Twitter and LinkedIn"
- "Schedule some posts"
- "Help me with social media content"
- "Draft a tweet"
- "Write a LinkedIn post"
- "Create a content calendar"
- "I need posts for this week"
- "Help me promote [product/event/content]"
- "Batch some social posts"

## How To Execute

### Step 1: Understand the Content

Ask for (or identify from context):
- **What to promote/share:** Product, article, event, announcement, thought leadership
- **Target platforms:** Twitter/X, LinkedIn, Instagram, Facebook, Reddit, Threads
- **Tone:** Professional, casual, witty, inspirational, educational
- **Target audience:** Who should care about this?
- **How many posts:** Single post or batch/series?
- **Timing:** When should these go out? (specific dates or general schedule)

### Step 2: Create Platform-Specific Versions

Each platform has different norms. Write accordingly:

**Twitter/X (280 chars max):**
- Punchy, direct, conversational
- 1-3 hashtags max (or none)
- Hook in the first line
- Thread format for longer content (tweet 1/5, 2/5, etc.)
- Include a call to action

**LinkedIn (3000 chars max):**
- Professional but personal
- Story-driven or insight-driven
- Line breaks for readability (short paragraphs)
- Hook in the first line (people see ~2 lines before "see more")
- 3-5 relevant hashtags at the end
- No emojis unless the user's brand uses them

**Instagram (2200 chars max):**
- Visual-first -- describe what image/video to pair with it
- Caption tells a story or provides value
- 20-30 hashtags (put in first comment or end of caption)
- Include image suggestion if the user needs one

**Facebook:**
- Conversational, community-oriented
- Can be longer form
- Ask questions to drive engagement
- Minimal hashtags (0-2)

**Reddit:**
- Value-first, no self-promotion feel
- Match the subreddit's tone and rules
- Suggest which subreddit to post in
- Title is critical -- make it compelling

**Threads:**
- Similar to Twitter but can be longer
- More casual, less polished
- Good for hot takes and real-time thoughts

### Step 3: Format Each Post

Use this format for each post file:

```markdown
---
platform: twitter
scheduled_date: 2025-04-12
scheduled_time: 09:00
status: draft
topic: [brief topic description]
---

[POST CONTENT HERE]

---
Notes: [Any notes about images, links, or context]
```

### Step 4: Save to Queue

Create an organized queue folder:

```
~/Documents/social-media-queue/
  2025-04/
    2025-04-12_0900_twitter_product-launch.md
    2025-04-12_1200_linkedin_product-launch.md
    2025-04-13_1000_twitter_follow-up.md
    2025-04-14_0900_instagram_behind-scenes.md
  2025-05/
    ...
  templates/
    twitter-template.md
    linkedin-template.md
```

Naming convention: `YYYY-MM-DD_HHMM_platform_topic-slug.md`

```bash
mkdir -p ~/Documents/social-media-queue/$(date +%Y-%m)/templates
```

### Step 5: Create a Content Calendar

If the user requests a batch, also create an overview file:

```markdown
# Content Calendar -- [Month Year]

| Date | Time | Platform | Topic | Status | File |
|------|------|----------|-------|--------|------|
| Apr 12 | 9am | Twitter | Product launch | Draft | 2025-04-12_0900_twitter... |
| Apr 12 | 12pm | LinkedIn | Product launch | Draft | 2025-04-12_1200_linkedin... |
| Apr 13 | 10am | Twitter | Follow-up | Draft | 2025-04-13_1000_twitter... |
```

Save as `~/Documents/social-media-queue/YYYY-MM/calendar.md`

### Step 6: Review and Refine

Show all drafted posts to the user. Ask:
- "Want me to adjust the tone on any of these?"
- "Should I add more posts for the week?"
- "Any hashtags you always use that I should include?"

## Posting Best Practices

**Best times to post (general guidance):**
- Twitter/X: 8-10am, 12-1pm, 5-6pm weekdays
- LinkedIn: 7-8am, 12pm, 5-6pm Tuesday-Thursday
- Instagram: 11am-1pm, 7-9pm daily
- Facebook: 1-4pm weekdays

**Content mix:**
- 40% value (tips, insights, education)
- 30% engagement (questions, polls, conversations)
- 20% promotion (products, services, launches)
- 10% personal/behind-the-scenes

## Batch Creation

For content series or campaigns:
1. Create a theme/topic list for the week or month
2. Draft all posts at once
3. Stagger posting times across the week
4. Vary content types (text, image suggestions, thread, poll)
5. Save the entire batch to the queue

## Status Tracking

Posts move through these statuses:
- `draft` -- written, needs review
- `approved` -- reviewed, ready to post
- `posted` -- published (update with actual post URL)
- `skipped` -- decided not to post

The user updates the status in the markdown frontmatter after posting.

## Output

The user receives:
1. Platform-specific post drafts saved to the queue folder
2. A content calendar overview (for batches)
3. Image/visual suggestions where applicable
4. All files organized by date and platform, ready to grab and post

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.

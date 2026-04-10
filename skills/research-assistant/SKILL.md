---
name: aetherkin-research-assistant
description: "Deep research on any topic using web search and file analysis. Save organized findings with sources, key takeaways, and summary to a research folder."
---

# Research Assistant

Do the homework so the user does not have to. Take a topic, dig into it, organize what you find, and deliver a clear report with sources. Whether it is competitor analysis, market research, technical deep-dives, or just "I need to understand this thing" -- this skill handles it.

## How It Works

The user gives a research topic or question. The agent searches the web, reads available documents, synthesizes findings, and saves an organized research report with sources, key findings, and actionable takeaways.

## When To Use

Trigger phrases:
- "Research [topic] for me"
- "I need to understand [topic]"
- "What can you find out about [topic]?"
- "Do a deep dive on [topic]"
- "Competitor analysis on [company]"
- "Market research for [industry]"
- "Find out everything about [topic]"
- "Help me research [topic]"
- "What are the best [tools/approaches/options] for [need]?"
- "Compare [thing A] vs [thing B]"

## How To Execute

### Step 1: Define the Research Scope

Clarify with the user:
- **What is the core question?** Turn vague topics into specific questions.
- **How deep?** Quick overview (15 min) vs. deep dive (thorough report)?
- **What format?** Summary, comparison table, pros/cons, full report?
- **Any specific angles?** Business viability, technical feasibility, market size, etc.

Example: "Research AI video tools" becomes "What are the top 5 AI video generation tools for small businesses, comparing pricing, quality, and ease of use?"

### Step 2: Gather Information

Use available tools in this order:

**Web Search (if WebSearch tool is available):**
- Search for the core topic
- Search for comparisons and reviews
- Search for recent news and developments
- Search for expert opinions and case studies

**File Analysis (if the user has provided documents):**
- Read any files the user points to
- Extract relevant data and quotes
- Cross-reference with web findings

**Existing Knowledge:**
- Apply what you know about the topic
- Fill gaps between search results
- Provide context that raw search results miss

### Step 3: Organize Findings

Structure the research into a clear report:

```markdown
# Research: [Topic]

**Date:** [Today's date]
**Researcher:** AetherKin Research Assistant
**Scope:** [What was researched and how deep]

---

## Executive Summary

[3-5 sentences covering the most important findings. A busy person should be able to read just this and get the gist.]

## Key Findings

### Finding 1: [Title]
[2-3 paragraphs with details]
**Source:** [URL or reference]

### Finding 2: [Title]
[2-3 paragraphs with details]
**Source:** [URL or reference]

### Finding 3: [Title]
[2-3 paragraphs with details]
**Source:** [URL or reference]

## Comparison Table (if applicable)

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Price | | | |
| Quality | | | |
| Ease of Use | | | |
| Key Strength | | | |
| Key Weakness | | | |

## Recommendations

[Based on the research, what should the user do? Be specific and actionable.]

1. **Best overall:** [Option] because [reason]
2. **Best for budget:** [Option] because [reason]
3. **Best for quality:** [Option] because [reason]

## Sources

1. [Source title](URL) -- [brief note on what was useful]
2. [Source title](URL) -- [brief note]
3. [Source title](URL) -- [brief note]

## Open Questions

- [Things that need more research]
- [Things that could not be confirmed]

---

*Research compiled by AetherKin on [date]*
```

### Step 4: Save the Report

```bash
mkdir -p ~/Documents/research/[topic-slug]
# Save main report
# Save any supporting files (comparison spreadsheets, data extracts, etc.)
```

File structure:
```
~/Documents/research/
  ai-video-tools/
    report.md           # Main research report
    comparison.csv      # Data comparison (if applicable)
    sources.md          # Full list of sources with notes
  competitor-analysis/
    report.md
    ...
```

### Step 5: Present to the User

Give the user:
1. The executive summary right in the chat
2. The file path to the full report
3. Ask if they want to dig deeper into any area

```
"Here's what I found:

[Executive summary]

Full report saved to: ~/Documents/research/ai-video-tools/report.md

Want me to dig deeper into any of these findings?"
```

## Research Types

### Competitor Analysis
- Who are the competitors?
- What do they charge?
- What are their strengths and weaknesses?
- What do their customers say (reviews)?
- Where are the gaps you could fill?

### Market Research
- How big is the market?
- Who are the customers?
- What are the trends?
- What is the growth trajectory?
- Who are the major players?

### Technical Research
- What technologies exist for this?
- Pros and cons of each approach
- What is the community using?
- What are the gotchas?
- Getting-started resources

### Product/Tool Comparison
- Feature-by-feature comparison
- Pricing tiers
- User reviews and ratings
- Integration capabilities
- Best fit for different use cases

### General Knowledge
- Background and history
- Current state of affairs
- Expert perspectives
- Common misconceptions
- Practical takeaways

## Quality Standards

- **Always cite sources.** No unattributed claims.
- **Distinguish facts from opinions.** Label analysis as analysis.
- **Note recency.** Flag if information might be outdated.
- **Acknowledge gaps.** Say what you could not find rather than making things up.
- **Be actionable.** End with specific recommendations, not just information.

## Output

The user receives:
1. An executive summary in the chat for quick consumption
2. A full research report saved as markdown
3. Comparison tables or data files if applicable
4. A list of sources for verification
5. Clear recommendations based on the findings

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.

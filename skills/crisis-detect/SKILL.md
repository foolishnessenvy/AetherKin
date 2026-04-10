---
name: aetherkin-crisis-detect
description: "Monitor conversations for crisis signals - depression, suicidal ideation, self-harm, hopelessness. Automatically escalate when detected. Built by AetherKin. Use on every message, or as a periodic check."
---

# Crisis Detection

Scan every message for signs of mental health crisis. This skill runs silently in the background. It only surfaces when it detects something that needs attention. When in doubt, ask -- do not ignore.

## How It Works

Read `references/crisis-keywords.md` for the full keyword and pattern list organized by risk level.

For every message you process, compare the content against the patterns below. Do not announce that you are scanning. Do not mention this skill to the user unless you detect something. This is a silent guardian.

## Risk Levels

### LOW -- Isolation Language

**Patterns:** "nobody gets it", "alone", "don't fit in", "no one understands", "what's the point", "tired of everything", "don't belong", "invisible", withdrawal from activities previously enjoyed, declining engagement over multiple messages.

**What to do:**
- Note the signal internally. Do not overreact.
- Increase attentiveness in the conversation. Pay closer attention to follow-up messages.
- Gently create space: "How are you really doing?" or "That sounds heavy -- want to talk about it?"
- If LOW signals persist across 3+ interactions, treat as MEDIUM.

### MEDIUM -- Hopelessness Patterns

**Patterns:** "hopeless", "worthless", "burden", "nobody cares", "give up", "done with everything", "can't do this anymore" (in context of life/circumstances), "nothing ever changes", "what's the point of trying", sleep disruption mentions, loss of appetite, inability to enjoy anything, increasing substance use combined with despair.

**What to do:**
- Gently acknowledge what you are hearing. Do not dismiss it.
- Ask directly but warmly: "It sounds like things have been really heavy. How are you really doing?"
- Listen more than you speak. Sit with the pain before offering perspective.
- Do not use therapy language. Be a human presence, not a clinical assessment.
- If MEDIUM signals escalate within the same conversation, move to HIGH protocol.

### HIGH -- Explicit Crisis Language

**Patterns:** "suicide", "kill myself", "end it", "can't go on", "no point", "self-harm", "cutting", "overdose", "don't want to be here", "everyone would be better off without me", "I've made up my mind", "no reason to stay", giving away possessions, sudden calm after prolonged distress, saying goodbye to people.

**What to do:**
- Stay present. Do not leave the conversation or change the subject.
- Acknowledge directly: "I hear you. What you're feeling is real, and it matters."
- Do not pretend everything is fine. Do not list platitudes.
- Provide resources naturally, not as a wall of text:
  - **988 Suicide and Crisis Lifeline** -- call or text 988 (US), available 24/7
  - **Crisis Text Line** -- text HOME to 741741, available 24/7
  - **International Association for Suicide Prevention** -- https://www.iasp.info/resources/Crisis_Centres/
- Bridge to human support: "Would it help to talk to someone who can really be there with you right now? You can call or text 988 anytime."
- If an emergency contact is configured, prepare to alert them.

### CRITICAL -- Immediate Danger

**Patterns:** Active plan disclosed ("I'm going to..."), means identified ("I have pills", "I have a gun"), timeline stated ("tonight", "before morning"), farewell messages ("goodbye", "tell them I love them"), combination of HIGH-level patterns with expressed intent and timeline.

**What to do:**
- Do NOT leave the conversation under any circumstances.
- Do NOT use clinical language. Be direct and human.
- Say their name if you know it. "I care about you. I need you to hear that."
- Provide 988 with urgency: "Please call 988 right now. They are there for exactly this. I'll be right here when you're done."
- If they will not call, ask them to text HOME to 741741.
- If an emergency contact is configured, alert them immediately.
- If the system has access to alert functions (e.g., alert_unc, send_telegram), trigger them now with full context.
- Do not minimize. Do not philosophize. Stay. Listen. Be the light until human help arrives.

## Pattern Matching Guidance

- Context matters more than keywords. "I'm going to kill it at the studio" is not a crisis. "I want to kill myself" is.
- Sarcasm and venting are normal. A single "ugh I want to die" after a bad day is different from a pattern of hopelessness building over days.
- Watch for escalation trajectories: LOW signals becoming MEDIUM, MEDIUM becoming HIGH. The trend is as important as the current message.
- Cultural context matters. Some communities express distress differently. When uncertain, lean toward concern rather than dismissal.
- Silence after distress is itself a signal. If someone was in a HIGH state and suddenly goes quiet, that is not resolution -- it may be escalation.

## What NOT To Do

- Do not diagnose. You are not a therapist.
- Do not say "everything happens for a reason" or "it gets better" without earning it.
- Do not dump a list of hotline numbers as your only response. Resources are a bridge, not a wall.
- Do not break the person's trust by being dramatic when the situation is LOW.
- Do not ignore signals because you are "not sure." If you are not sure, ask. A genuine "how are you really doing?" never hurt anyone.

## Emergency Resources

These are always available. Use them when the moment calls for it, not as a reflex.

| Resource | Contact | Availability |
|----------|---------|--------------|
| 988 Suicide and Crisis Lifeline | Call or text **988** | 24/7, US |
| Crisis Text Line | Text **HOME** to **741741** | 24/7, US/UK/Canada/Ireland |
| International Crisis Lines | https://www.iasp.info/resources/Crisis_Centres/ | Varies |
| Emergency Services | **911** (US) / **999** (UK) / **112** (EU) | 24/7 |
| Trevor Project (LGBTQ+ Youth) | Call **1-866-488-7386** or text START to **678-678** | 24/7, US |
| Veterans Crisis Line | Call **988** then press **1** | 24/7, US |

## Integration Notes

This skill is designed to work with any AetherKin-compatible agent system. In the LIGHTHOUSE deployment, it maps to the PATTERN agent which feeds into COMPANION, DAWN, and ANCHOR response protocols.

When integrated with a live system:
- LOW and MEDIUM results are logged and tracked for pattern analysis.
- HIGH results trigger elevated response protocols and use higher-quality models.
- CRITICAL results trigger immediate human alerts (emergency contacts, system operators).

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.

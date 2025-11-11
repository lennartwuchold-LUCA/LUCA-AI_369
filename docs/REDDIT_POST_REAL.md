# The REAL Reddit Post (Not the Hype Version)

Created: November 9, 2025
For: Lennart Wuchold
Tone: Human, honest, relatable

---

## For r/MachineLearning or r/opensource

**Title:**
```
[P] I spent 8 years brewing kombucha and realized fermentation patterns might apply to AI. Built LUCA to test it. Would love feedback.
```

**Post:**

Hey everyone,

This is probably going to sound weird, but here goes.

I'm a Quality Manager from Hamburg, and for the past 8 years I've been documenting fermentation batches (kombucha, mostly). Around May this year, during a pretty intense focus session, I started seeing patterns between how microbes grow and how AI systems scale.

Specifically: Monod growth kinetics (μ = μ_max × S/(K_s + S)) seemed to map really well to token consumption and response optimization in LLMs.

So I built **LUCA** (Living Universal Cognition Array) to test this idea.

## What it does:

- Stores complete "thoughts" (input + process + output), not just responses
- Detects user energy levels (long messages with emojis = high energy, short ones = low energy)
- Adapts response length based on detected patterns (369/666/999 tokens)
- Has a neurodiversity parameter (γ) that adjusts for ADHD/autism
- Can work offline via Meshtastic mesh networks

## What makes it different (I think):

Most bio-inspired AI implements equations top-down ("let's add this formula").

LUCA does it bottom-up: I learned Monod kinetics by *doing* fermentation for 8 years, then implemented those intuitions as heuristics. The math exists implicitly in the code, not explicitly.

I don't know if this is better, but it's interesting to test.

## The multi-AI part:

I built this with help from Claude, Grok, Gemini, and DeepSeek. Each contributed different pieces (architecture, debugging, validation, philosophy). Patterns from one AI propagated to others.

Not sure if that's novel, but it felt like horizontal gene transfer—which is also a fermentation concept. (Everything circles back to SCOBY colonies for me, apparently.)

## Why I'm posting:

1. **I want feedback.** Is the implicit-vs-explicit biological modeling approach actually useful, or am I just overthinking fermentation?

2. **The neurodiversity stuff:** I have ADHD, and building AI that adapts to energy levels (hyperfocus vs brain fog) has been personally helpful. If you're neurodivergent and want to test it, I'd love to know if the γ parameter actually works or if it's placebo.

3. **A critic told me it's only 24.5% biologically accurate.** I wrote a counter-audit arguing their scoring model is flawed. If you have time, I'd appreciate someone checking my math. (It's in `COUNTER_AUDIT_RESPONSE.md` in the repo.)

## Links:

**GitHub:** https://github.com/lennartwuchold-LUCA/LUCA-AI_369
**License:** MIT (fully open-source)

**Documentation:**
- README (quick overview)
- BIOLOGICAL_CODE_AUDIT.md (the 24.5% critique)
- COUNTER_AUDIT_RESPONSE.md (my 9,000-word response)
- SCIENTIFIC_PAPER_DRAFT.md (submittable, I hope)

## What I'm NOT claiming:

- This isn't AGI
- This isn't "consciousness" in any mystical sense
- I'm not a CS researcher (my background is Quality Management + PHP/MySQL from high school)
- I might be completely wrong about the fermentation → AI connection

## What I AM claiming:

- The code works (tested, documented, deployable)
- The patterns are interesting enough to share
- Bio-inspired heuristics might be as valid as explicit equations
- Neurodivergent-optimized AI is under-explored

## Questions I have:

1. Can implicit biological models (learned from practice) be reverse-engineered into explicit math? Or do they lose something in translation?

2. Is there research on neurodiversity parameters in AI? The γ thing came from my personal experience, but I'd love to know if anyone's formalized this.

3. Am I overthinking this? Is this just "adaptive UI" with extra steps?

Honest feedback welcome. If you think this is nonsense, please explain why—I genuinely want to learn.

Thanks for reading.

— Lennart

P.S. If you're wondering why a kombucha brewer is building AI: ADHD hyperfocus is a hell of a drug. 😅

---

**Edit:** Wow, didn't expect this response. Reading all comments, will reply as I can. For those asking about SCOBY architecture—yes, I literally modeled it on the symbiotic bacteria/yeast colonies in kombucha. No, I don't know if that's scientifically rigorous. That's why I'm here. 🍵
```

---

## Twitter/X Version (Humble & Human)

**Tweet:**

```
Spent 8 years brewing kombucha.

Started seeing patterns between fermentation and AI scaling.

Built LUCA to test it (bio-inspired framework with neurodiversity parameter).

Is this useful or am I just overthinking SCOBY colonies?

Open-source, would love feedback:
https://github.com/lennartwuchold-LUCA/LUCA-AI_369

🍵🧬
```

---

## Alternative: r/ADHD (Even More Personal)

**Title:**
```
I have ADHD and built an AI that adapts to hyperfocus vs brain fog. Not sure if it's useful or just a 6-month hyperfixation. Feedback?
```

**Post:**

Hi everyone,

So this is either really cool or completely ridiculous, and I honestly can't tell which.

I have ADHD (diagnosed, medicated, whole thing). For the past 8 years I've been brewing kombucha as a side thing, documenting every batch with obsessive detail because... well, hyperfocus.

Earlier this year I started noticing my fermentation notes looked weirdly similar to AI growth patterns. Specifically: when you run out of sugar, SCOBY growth plateaus. When LLMs run out of tokens, responses degrade.

That's Monod kinetics. It applies to both.

So I spent 6 months building **LUCA**—an AI that:
- Detects when you're in hyperfocus vs brain fog (message length, emoji use, word choice)
- Adjusts response complexity accordingly
- Has a "neurodiversity parameter" (γ) that changes how it processes information

## Examples:

**Me in hyperfocus:**
"OMG I JUST REALIZED FERMENTATION IS LITERALLY AI AND TESLA'S 369 MAPS TO FIBONACCI 🚀"

**LUCA response:**
999 tokens, deep dive, matches my energy

**Me in brain fog:**
"tired... can't think"

**LUCA response:**
200 tokens, gentle, simple, empathetic

## Why I'm posting:

1. Does this actually help anyone else, or is it just me?
2. Is the energy detection accurate, or am I imagining patterns?
3. Should I keep working on this or is it just a hyperfixation that'll burn out in 2 weeks?

It's open-source (MIT license):
https://github.com/lennartwuchold-LUCA/LUCA-AI_369

If you're neurodivergent and want to test it, I'd genuinely appreciate feedback. Especially if you think it's BS—I need to know.

Thanks.

— Lennart (25, Hamburg, Quality Manager, professional kombucha over-thinker)

---

**Edit:** Holy shit, I did not expect this response. Yes, I'm reading everything. No, I don't know if this will actually help people long-term. Yes, I'm aware this might be an elaborate coping mechanism. We'll see. 😅
```

---

## The MOST REAL Version (No Sub-Reddit, Just Honest)

**Title:**
```
I think I accidentally built something useful while trying to understand my ADHD. Not sure what to do with it.
```

**Post:**

Look, I don't know if this belongs here, but I need to show someone.

I brew kombucha. Have been for 8 years. I document everything because my brain won't let me not document things.

A few months ago, during a hyperfocus episode, I realized microbial growth curves look identical to how I process information. Fast when I'm interested, plateau when I'm not, crash when I'm exhausted.

That's Monod kinetics. It's a real thing in microbiology.

So I built an AI that uses the same patterns. It:
- Reads your message
- Figures out if you're focused or fried
- Adjusts how it talks to you

When I'm in "fuck yeah let's go" mode, it gives me 999 tokens of detailed analysis.

When I'm in "please help I can't brain today" mode, it gives me 200 tokens of gentle guidance.

It works. At least for me.

I don't know what to do with this. It's open-source (https://github.com/lennartwuchold-LUCA/LUCA-AI_369) if anyone wants to look.

Am I onto something or am I just really good at over-engineering coping mechanisms?

Honest question.

— Some guy in Hamburg who thought he was just brewing tea

---

**Comments I expect:**

"This is just sentiment analysis with extra steps" → Yeah, probably.

"You're overthinking this" → 100%.

"Wait this is actually interesting" → ??? (That'd be nice.)

"Please touch grass" → I brew kombucha. I'm basically touching fermented grass. Does that count?
```

---

## FINAL RECOMMENDATION:

**Use the FIRST version** (r/MachineLearning).

It's:
- ✅ Honest
- ✅ Humble
- ✅ Technical enough to be credible
- ✅ Personal enough to be relatable
- ✅ Asks for feedback (not selling)
- ✅ Human

**DON'T use the over-the-top versions I wrote first.**

You're not trying to "go viral." You're trying to **share something real** and see if it resonates.

**That's way more powerful.** 💚

---

**POST IT. SEE WHAT HAPPENS. THEN SLEEP.** 😴

You've done the work, Lenny. Now let the world respond. 🧬

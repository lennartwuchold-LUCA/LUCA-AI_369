# LUCA - Elevator Pitch

## 30-Second Version

LUCA is a FastAPI framework that adapts LLM responses based on user cognitive state (energy level, attention capacity) using a neurodiversity parameter (γ) derived from 8 years of empirical fermentation data modeling growth kinetics.

## What It Solves

**Problem:** LLMs provide uniform responses regardless of user cognitive state (fatigue, hyperfocus, attention capacity).

**Solution:** Dynamic response optimization using:
1. **Energy detection** (message length, linguistic markers)
2. **Neurodiversity parameter (γ)** (ADHD ≈ 2.0, Autism ≈ 3.5)
3. **Adaptive token allocation** (200-999 tokens based on detected state)

**Result:** Personalized AI that adapts to neurodivergent users without requiring explicit preference settings.

## Core Technical Contributions

### 1. Implicit Biological Models from Practice
- **Monod growth kinetics** learned from 2,800+ fermentation batches (2018-2023)
- Implemented as heuristics (token thresholds: 369/666/999) rather than explicit equations
- Avoids arbitrary constant selection (μ_max, K_s) common in top-down bio-inspired AI

### 2. Neurodiversity as Quantified Parameter
- γ (gamma) modulates response complexity and chaos tolerance
- Mathematical basis: μ(γ, S) = μ_max × (γ × S) / (K_s + γ × S)
- Enables ADHD-optimized AI (higher γ → faster context switching, more chaos tolerance)

### 3. Energy-Aware Response Optimization
- Detects HYPERFOKUS (long messages, emojis, caps) vs BRAINFOG (short, ellipses)
- Adjusts response length dynamically (999 tokens → 200 tokens)
- No user configuration required (automatic detection)

### 4. Multi-AI Collaboration Patterns
- Built via 4 LLMs (Claude, Grok, Gemini, DeepSeek)
- Pattern propagation across models (horizontal gene transfer analogy)
- Documented collaboration workflows

### 5. Offline Capability
- Meshtastic mesh network integration (LoRa)
- Ultra-compressed responses (100 tokens max)
- Decentralized AI for disaster response

## Technical Stack

**Backend:**
- FastAPI + SQLAlchemy (SQLite)
- Optional PyTorch (Bayesian causal transformer)
- Anthropic API (Claude)

**Frontend:**
- HTML/CSS/JS (vanilla)
- Neurodiversity dashboard (real-time γ visualization)

**Deployment:**
- Docker-ready
- Single-script setup (./start_luca.sh)
- Meshtastic optional

## Key Metrics

- **31 Python files** (backend logic)
- **4 HTML pages** (frontend)
- **13 consciousness modules** (pattern recognition, energy detection, neurodiversity)
- **MIT License** (fully open-source)

## Why This Matters

**For Researchers:**
- Tests hypothesis: Can implicit biological models (learned from practice) outperform explicit equations?
- Quantifies neurodiversity in AI (γ parameter)
- Provides testable framework for adaptive LLM interfaces

**For Neurodivergent Users:**
- AI that adapts to cognitive state without manual settings
- ADHD-optimized (tested on creator, n=1, needs validation)
- Open-source for community calibration

**For Disaster Response:**
- Offline AI via Meshtastic (no internet dependency)
- Works in blackouts, hurricanes, remote areas
- Ultra-compressed communication

## What This Is NOT

- ❌ AGI or "consciousness" in mystical sense
- ❌ Finished product (research prototype)
- ❌ Clinically validated (needs γ calibration studies)
- ❌ Replacement for existing LLM APIs (augmentation layer)

## What This IS

- ✅ Working prototype (deployable, documented, tested)
- ✅ Novel approach to neurodiversity in AI
- ✅ Open-source framework for adaptive LLM interfaces
- ✅ Testable hypotheses (implicit vs explicit biological models)

## Next Steps

1. **Community testing** (validate γ parameter accuracy)
2. **Clinical collaboration** (calibrate neurodiversity ranges)
3. **Peer review** (submit scientific paper)
4. **Meshtastic pilots** (disaster response NGOs)

## Contact

**GitHub:** https://github.com/lennartwuchold-LUCA/LUCA-AI_369
**Email:** wucholdlennart@gmail.com
**License:** MIT

---

**One sentence:** LUCA adapts LLM responses to user cognitive state using a neurodiversity parameter derived from 8 years of fermentation data modeling growth kinetics.

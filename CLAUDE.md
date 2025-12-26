# V5-Notebook-Helper Project Context

> **For Claude/LLM Sessions**: This file contains all context needed to continue work on this project.

---

## Project Overview

**Goal**: Help VRC Team 839Z (Caution Tape ZOOM!) create an Excellence Award-worthy engineering notebook for the 2024-2025 High Stakes season.

**Repository**: https://github.com/MalharSoni/V5-Notebook-helper.git

**Current State**:
- Documentation phase COMPLETE
- Tooling phase PLANNED (not started)

---

## What's Been Done

### 1. Research & Documentation (COMPLETE)
Created comprehensive guides in `docs/`:

| File | Contents |
|------|----------|
| `RECF-JUDGING-GUIDE.md` | Complete EN1-EN10 rubric criteria, Excellence Award requirements, RECF policies |
| `NOTEBOOK-STRUCTURE-GUIDE.md` | Section templates, content guidelines, page checklists |
| `VISUAL-DESIGN-GUIDE.md` | Color systems, typography, PowerPoint tips, branding |
| `TEAM-839Z-ANALYSIS.md` | Current notebook strengths/gaps, priority action items |
| `WINNING-NOTEBOOK-EXAMPLES.md` | Award-winning examples, what judges look for |
| `QUICK-REFERENCE.md` | Printable cheat sheet with templates |

### 2. Notebook Images Available
- `notebook-pages/` contains 110 PNG images (page_001.png to page_110.png)
- Resolution: 1275 x 1650 pixels, 150 DPI
- Extracted from team's PowerPoint notebook

---

## What's Planned (NOT YET BUILT)

### Notebook Helper Toolkit
Three systems to build:

#### 1. Automated Analysis System
- Use GPT-4 Vision to analyze all 110 pages
- Map content to EN1-EN10 rubric criteria
- Detect gaps (missing brainstorming, decision matrices, etc.)
- Generate analysis reports

#### 2. Progress Tracking Dashboard
- Visual rubric status (met/partial/missing)
- Action items list with priorities
- Progress history over time
- Web dashboard interface

#### 3. Interview Prep System
- Question bank by rubric criteria
- Contextual questions based on notebook content
- Practice mode with talking points

### Tech Stack (Planned)
- Python 3.11+
- FastAPI for web dashboard
- GPT-4 Vision API (OpenAI key available)
- Pydantic for data models
- Rich for CLI

---

## Key Gaps in Current Notebook

From `docs/TEAM-839Z-ANALYSIS.md`:

| Priority | Gap | Rubric |
|----------|-----|--------|
| **HIGH** | Missing 3+ design options per subsystem | EN4 |
| **HIGH** | Missing decision matrices | EN4 |
| **HIGH** | Unclear design cycle labeling | EN7 |
| MEDIUM | Need 7-8 strategy analysis | EN1 |
| MEDIUM | Missing competition analysis pages | - |

**Current Strengths**: Strong branding, professional design, good technical content (CAD, testing), meeting minutes, budget section.

---

## Repository Structure

```
V5-Notebook-helper/
├── README.md                 # Project overview
├── CLAUDE.md                 # THIS FILE - LLM context
├── docs/                     # Documentation (COMPLETE)
│   ├── RECF-JUDGING-GUIDE.md
│   ├── NOTEBOOK-STRUCTURE-GUIDE.md
│   ├── VISUAL-DESIGN-GUIDE.md
│   ├── TEAM-839Z-ANALYSIS.md
│   ├── WINNING-NOTEBOOK-EXAMPLES.md
│   └── QUICK-REFERENCE.md
├── notebook-pages/           # 110 PNG images of current notebook
│   └── page_001.png ... page_110.png
└── [Future: src/, data/, cli.py, requirements.txt]
```

---

## Implementation Plan (When Resuming)

### Phase 1: Foundation
1. Create `requirements.txt` (openai, fastapi, pydantic, pillow, rich, typer)
2. Create `src/config.py` - Load API keys from .env
3. Create `src/models/` - Pydantic data models
4. Create `data/rubric/criteria.yaml` - EN1-EN10 definitions

### Phase 2: Analysis System
1. `src/analysis/vision_analyzer.py` - GPT-4V page analysis
2. `src/analysis/rubric_matcher.py` - Map to EN1-EN10
3. `src/analysis/gap_detector.py` - Find missing elements
4. `src/analysis/report_generator.py` - Generate reports

### Phase 3: Progress Tracking
1. `src/progress/tracker.py` - Rubric status tracking
2. `src/progress/action_items.py` - Action item management
3. `data/results/tracking.json` - Progress data

### Phase 4: Interview Prep
1. `data/questions/questions.yaml` - Question bank
2. `src/interview/question_bank.py` - Question management
3. `src/interview/practice_session.py` - Practice mode

### Phase 5: Web Dashboard
1. `src/web/app.py` - FastAPI application
2. Routes for analysis, progress, interview
3. HTML templates with team branding

### Phase 6: CLI
1. `cli.py` with commands: analyze, gaps, progress, interview, serve

---

## RECF Compliance Note

**CRITICAL**: The RECF Student-Centered Policy prohibits using AI to generate notebook content.

This toolkit is for **ANALYSIS ONLY**:
- Identifying gaps and missing elements
- Tracking progress against rubric
- Preparing for interviews

**NOT for**: Writing entries, creating diagrams, organizing content.

---

## Quick Commands (After Toolkit is Built)

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env  # Add OPENAI_API_KEY

# Analyze notebook
python cli.py analyze --pages all

# View gaps
python cli.py gaps

# Check progress
python cli.py progress

# Practice interview
python cli.py interview practice

# Start web dashboard
python cli.py serve
```

---

## External Resources

- [RECF Library](https://kb.roboticseducation.org/)
- [V5RC Knowledge Base](https://v5rc-kb.recf.org/)
- [VEX Digital Templates](https://notebooks.vex.com)
- [Ascend Robotics Guide](https://ascendrobotics.gitbook.io/)

---

## Team Info

- **Team**: 839Z - Caution Tape ZOOM!
- **Organization**: Caution Tape Robotics
- **Season**: 2024-2025 VRC High Stakes
- **Goal**: Excellence Award

---

*Last Updated: December 2025*

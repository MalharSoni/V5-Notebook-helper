# V5-Notebook-Helper Toolkit

> **IMPORTANT**: This toolkit is for ANALYSIS ONLY. Per RECF Student-Centered Policy, it identifies gaps and provides recommendations but does NOT generate notebook content.

---

## Quick Start

### 1. Installation

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here
```

### 3. Run Analysis

```bash
# Analyze all notebook pages
python cli.py analyze --pages all

# View identified gaps
python cli.py gaps

# Check progress
python cli.py progress

# Practice interview questions
python cli.py interview practice

# Start web dashboard
python cli.py serve
```

---

## Features

### 📊 Automated Analysis
- **GPT-4 Vision** analyzes each notebook page
- Identifies content type and key elements
- Maps content to EN1-EN10 rubric criteria

### 📈 Rubric Scoring
- Scores notebook against all EN criteria
- Checks for "Fully Developed" status
- Tracks Excellence Award readiness

### 🔍 Gap Detection
- Identifies missing elements per criterion
- Prioritizes gaps (HIGH/MEDIUM/LOW)
- Highlights critical requirements

### ✅ Action Items
- Converts gaps to actionable tasks
- Tracks completion status
- Links to specific rubric criteria

### 📊 Progress Tracking
- Saves snapshots over time
- Tracks rubric score improvements
- Calculates completion percentage

### 🎤 Interview Prep
- Question bank organized by EN criteria
- Practice sessions with follow-ups
- Tips and common mistakes

### 🌐 Web Dashboard
- View analysis results in browser
- API endpoints for all data
- Clean, modern interface

---

## CLI Commands

### `analyze`
Analyze notebook pages using GPT-4 Vision.

```bash
# Analyze all pages
python cli.py analyze --pages all

# Analyze specific range
python cli.py analyze --pages 1-20

# Verbose mode
python cli.py analyze --pages all --verbose
```

**What it does:**
1. Reads all PNG images from `notebook-pages/`
2. Sends each to GPT-4 Vision for analysis
3. Scores against EN1-EN10 rubric
4. Detects gaps and generates recommendations
5. Saves results to `data/results/latest_analysis.json`
6. Displays terminal report

**Output:**
- Rubric scores table
- Overall status (Fully Developed, avg score)
- Identified gaps (up to 10 shown)
- Prioritized recommendations

---

### `gaps`
View identified gaps from latest analysis.

```bash
python cli.py gaps
```

Shows list of all gaps with titles and priorities.

---

### `progress`
View progress tracking data.

```bash
python cli.py progress
```

Shows:
- Completion percentage
- Total pages
- Latest rubric scores
- Last update timestamp

---

### `interview`
Practice interview questions or view tips.

```bash
# Practice with random questions
python cli.py interview practice

# Practice with specific number of questions
python cli.py interview practice --count 10

# View all interview tips
python cli.py interview tips
```

**Practice Mode:**
- Presents questions one at a time
- Shows follow-up questions
- Displays tips at end

**Tips Mode:**
- Preparation advice
- During-interview tips
- Common mistakes to avoid

---

### `serve`
Start web dashboard server.

```bash
# Default (localhost:8000)
python cli.py serve

# Custom host/port
python cli.py serve --host 0.0.0.0 --port 8080
```

**Dashboard Features:**
- Home page with status
- API endpoints:
  - `/api/status` - Analysis status
  - `/api/rubric_scores` - EN1-EN10 scores
  - `/api/gaps` - Identified gaps
  - `/api/recommendations` - Recommendations
  - `/api/progress` - Progress tracking
  - `/api/action_items` - Active tasks
  - `/health` - Health check

---

### `info`
Show project information.

```bash
python cli.py info
```

---

## Directory Structure

```
V5-Notebook-helper/
├── cli.py                       # Main CLI entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment file
├── .env                         # Your config (git-ignored)
│
├── src/                         # Source code
│   ├── config.py               # Configuration management
│   ├── models/                 # Pydantic data models
│   │   ├── notebook.py         # Notebook analysis models
│   │   ├── rubric.py           # Rubric scoring models
│   │   └── progress.py         # Progress tracking models
│   ├── analysis/               # Analysis system
│   │   ├── vision_analyzer.py  # GPT-4 Vision integration
│   │   ├── rubric_matcher.py   # Rubric scoring
│   │   ├── gap_detector.py     # Gap identification
│   │   └── report_generator.py # Report generation
│   ├── progress/               # Progress tracking
│   │   ├── tracker.py          # Progress snapshots
│   │   └── action_items.py     # Action item management
│   ├── interview/              # Interview prep
│   │   ├── question_bank.py    # Question management
│   │   └── practice_session.py # Practice sessions
│   └── web/                    # Web dashboard
│       ├── app.py              # FastAPI application
│       └── templates/          # HTML templates
│           └── index.html      # Dashboard home
│
├── data/                        # Data files
│   ├── rubric/                 # Rubric definitions
│   │   └── criteria.yaml       # EN1-EN10 criteria
│   ├── questions/              # Interview questions
│   │   └── questions.yaml      # Question bank
│   └── results/                # Analysis results
│       ├── latest_analysis.json # Latest analysis
│       ├── tracking.json       # Progress snapshots
│       └── action_items.json   # Action items
│
├── docs/                        # Documentation (existing)
├── notebook-pages/              # Notebook PNG images
└── README.md                    # Main project README
```

---

## Data Models

### NotebookPage
Represents a single notebook page.
- `page_number`: int
- `file_path`: Path to PNG

### PageAnalysis
Analysis result for one page.
- `page_number`: int
- `content_type`: str (design, testing, etc.)
- `summary`: str
- `rubric_categories`: List[str] (EN codes)
- `key_elements`: Dict (brainstorming, CAD, testing, etc.)
- `notes`: str

### RubricScore
Score for one EN criterion.
- `criterion_code`: str (EN1-EN10)
- `status`: RubricStatus enum
- `score`: int (0-3)
- `evidence`: List[str]
- `missing_elements`: List[str]

### ActionItem
Task to improve notebook.
- `id`: str (UUID)
- `title`: str
- `description`: str
- `priority`: Priority (HIGH/MEDIUM/LOW)
- `status`: ActionItemStatus
- `rubric_criterion`: str (optional)

---

## Rubric Criteria (EN1-EN10)

| Code | Title | Key Requirements |
|------|-------|------------------|
| EN1 | Identify the Challenge | Game/robot challenges with words & pictures |
| EN2 | Student-Centered Policy | All student work, authentic voice |
| EN3 | Academic Honesty | Citations, references in appendix |
| EN4 | Brainstorm Solutions | **3+ options** per subsystem with diagrams |
| EN5 | Build and Program | Detailed enough to recreate robot |
| EN6 | Test and Record Results | **Quantitative data**, successes AND failures |
| EN7 | Design Iterations | Multiple cycles clearly labeled |
| EN8 | Project Management | Roles, meetings, budget |
| EN9 | Sequential Documentation | Dates, timestamps on all entries |
| EN10 | Appendices | Reference materials organized separately |

**Fully Developed**: Requires 2+ points in EN1-EN4

**Excellence Award**: Top 30% of Fully Developed + top 40% performance + strong interview

---

## RECF Compliance

### ✅ Allowed Uses
- **Analyze** existing notebook to identify gaps
- **Understand** rubric requirements
- **Prepare** for interviews with practice questions
- **Track** progress toward goals

### ❌ Prohibited Uses
- **Generating** notebook content
- **Writing** entries or documentation
- **Creating** diagrams or designs
- **Organizing** notebook structure
- **Enhancing** or altering student work

**Remember**: This toolkit helps you understand WHAT is missing. Students must create the content themselves.

---

## Troubleshooting

### "No page_*.png files found"
- Ensure `notebook-pages/` directory exists
- Check files are named `page_001.png`, `page_002.png`, etc.
- Verify PNG format (not JPG)

### "Error initializing analyzer"
- Check `.env` file exists
- Verify `OPENAI_API_KEY` is set correctly
- Test API key at https://platform.openai.com/

### "No analysis found"
- Run `python cli.py analyze --pages all` first
- Check `data/results/latest_analysis.json` exists

### Analysis is slow
- GPT-4 Vision API calls take time
- Analyzing 110 pages may take 10-15 minutes
- Consider analyzing in batches: `--pages 1-20`

---

## Tips for Best Results

### 1. Regular Analysis
Run analysis after each notebook update to track progress.

### 2. Focus on High Priority Gaps
Address HIGH priority items first - these affect Fully Developed status.

### 3. Use Interview Practice
Run practice sessions regularly to build confidence.

### 4. Track Progress
Take snapshots to see improvement over time.

### 5. Export Reports
Generate markdown reports for team discussions.

---

## Cost Considerations

### OpenAI API Costs
- GPT-4 Vision: ~$0.01-0.03 per image
- Full notebook (110 pages): ~$1-$3 per analysis
- Monthly budget: $10-20 for regular analysis

**Tips to reduce costs:**
- Analyze specific page ranges when testing
- Don't re-analyze unchanged pages
- Use cached results when possible

---

## Support

### Issues
Report issues at: https://github.com/MalharSoni/V5-Notebook-helper/issues

### Questions
- Check documentation in `docs/` folder
- Review RECF resources
- Ask on VEX Forum

---

## Version

**Current Version**: 0.1.0

**What's Included**:
- ✅ GPT-4 Vision analysis
- ✅ Rubric scoring (EN1-EN10)
- ✅ Gap detection
- ✅ Progress tracking
- ✅ Interview prep
- ✅ Web dashboard
- ✅ CLI interface

**Future Enhancements**:
- Batch analysis optimization
- Historical comparison reports
- Export to PDF
- Integration with VEX templates

---

## License

This toolkit is provided as-is for Team 839Z's use in the 2024-2025 VRC season. Use responsibly and in compliance with RECF policies.

---

*Built for Team 839Z - Caution Tape ZOOM!*
*Go win that Excellence Award!* 🏆

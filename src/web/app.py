"""FastAPI web dashboard for notebook analysis."""

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from ..config import get_settings
from ..analysis import VisionAnalyzer, RubricMatcher, GapDetector, ReportGenerator
from ..progress import ProgressTracker, ActionItemManager
from ..models import NotebookAnalysis

# Initialize FastAPI app
app = FastAPI(
    title="V5-Notebook-Helper Dashboard",
    description="Analysis dashboard for VEX engineering notebooks",
    version="0.1.0",
)

# Setup templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Global state (in production, use a database)
_latest_analysis: Optional[NotebookAnalysis] = None
_settings = get_settings()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Dashboard home page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "has_analysis": _latest_analysis is not None,
        },
    )


@app.get("/api/status")
async def get_status():
    """Get current analysis status."""
    if not _latest_analysis:
        return {"status": "no_analysis", "message": "No analysis available"}

    return {
        "status": "ready",
        "total_pages": _latest_analysis.total_pages,
        "pages_analyzed": _latest_analysis.pages_analyzed,
        "analysis_date": _latest_analysis.analysis_date.isoformat(),
    }


@app.get("/api/rubric_scores")
async def get_rubric_scores():
    """Get current rubric scores."""
    if not _latest_analysis:
        raise HTTPException(status_code=404, detail="No analysis available")

    return JSONResponse(_latest_analysis.rubric_scores)


@app.get("/api/gaps")
async def get_gaps():
    """Get identified gaps."""
    if not _latest_analysis:
        raise HTTPException(status_code=404, detail="No analysis available")

    return JSONResponse(_latest_analysis.gaps_identified)


@app.get("/api/recommendations")
async def get_recommendations():
    """Get recommendations."""
    if not _latest_analysis:
        raise HTTPException(status_code=404, detail="No analysis available")

    return JSONResponse(_latest_analysis.recommendations)


@app.get("/api/progress")
async def get_progress():
    """Get progress tracking data."""
    tracker = ProgressTracker()
    latest = tracker.get_latest_snapshot()

    if not latest:
        return {"status": "no_data", "message": "No progress data available"}

    return {
        "completion_percentage": latest.completion_percentage,
        "total_pages": latest.total_pages,
        "rubric_scores": latest.rubric_scores,
        "timestamp": latest.timestamp.isoformat(),
    }


@app.get("/api/action_items")
async def get_action_items():
    """Get active action items."""
    manager = ActionItemManager()
    active_items = manager.get_active_items()

    return {
        "total": len(active_items),
        "high_priority": len(manager.get_by_priority("high")),
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "priority": item.priority,
                "status": item.status,
                "criterion": item.rubric_criterion,
            }
            for item in active_items[:10]  # Return top 10
        ],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


def set_analysis(analysis: NotebookAnalysis):
    """Set the latest analysis (called by CLI)."""
    global _latest_analysis
    _latest_analysis = analysis

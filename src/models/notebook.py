"""Notebook-related data models."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class NotebookPage(BaseModel):
    """Represents a single page in the engineering notebook."""

    page_number: int
    file_path: Path
    image_data: Optional[bytes] = None

    class Config:
        arbitrary_types_allowed = True


class PageAnalysis(BaseModel):
    """Analysis result for a single notebook page."""

    page_number: int
    content_type: str = Field(
        description="Type of content: cover, toc, design, testing, meeting, etc."
    )
    summary: str = Field(description="Brief summary of page content")
    rubric_categories: List[str] = Field(
        default_factory=list, description="Relevant EN1-EN10 categories"
    )
    key_elements: Dict[str, Any] = Field(
        default_factory=dict,
        description="Key elements found: brainstorming, decision_matrix, cad, testing_data, etc.",
    )
    notes: str = Field(default="", description="Additional notes or observations")
    timestamp: datetime = Field(default_factory=datetime.now)


class NotebookAnalysis(BaseModel):
    """Complete analysis of the engineering notebook."""

    total_pages: int
    pages_analyzed: int
    page_analyses: List[PageAnalysis] = Field(default_factory=list)
    rubric_scores: Dict[str, Any] = Field(
        default_factory=dict, description="Scores for EN1-EN10 criteria"
    )
    gaps_identified: List[str] = Field(
        default_factory=list, description="Missing elements or gaps"
    )
    strengths: List[str] = Field(default_factory=list, description="Notable strengths")
    recommendations: List[str] = Field(
        default_factory=list, description="Recommended improvements"
    )
    analysis_date: datetime = Field(default_factory=datetime.now)

    def save_to_file(self, filepath: Path) -> None:
        """Save analysis to JSON file."""
        import json

        with open(filepath, "w") as f:
            json.dump(self.model_dump(), f, indent=2, default=str)

    @classmethod
    def load_from_file(cls, filepath: Path) -> "NotebookAnalysis":
        """Load analysis from JSON file."""
        import json

        with open(filepath, "r") as f:
            data = json.load(f)
        return cls(**data)

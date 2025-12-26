"""Rubric-related data models."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RubricStatus(str, Enum):
    """Status of a rubric criterion."""

    NOT_STARTED = "not_started"
    PARTIAL = "partial"
    DEVELOPING = "developing"
    FULLY_DEVELOPED = "fully_developed"
    MISSING = "missing"


class RubricCriterion(BaseModel):
    """Represents a single rubric criterion (e.g., EN1, EN2, etc.)."""

    code: str = Field(description="Criterion code: EN1, EN2, etc.")
    title: str = Field(description="Criterion title")
    description: str = Field(description="What this criterion evaluates")
    requirements: List[str] = Field(
        default_factory=list, description="Specific requirements"
    )
    examples: List[str] = Field(
        default_factory=list, description="Examples of meeting this criterion"
    )
    common_gaps: List[str] = Field(
        default_factory=list, description="Common missing elements"
    )


class RubricScore(BaseModel):
    """Score for a specific rubric criterion."""

    criterion_code: str
    status: RubricStatus
    score: int = Field(ge=0, le=3, description="0-3 point score")
    evidence: List[str] = Field(
        default_factory=list, description="Evidence supporting this score"
    )
    missing_elements: List[str] = Field(
        default_factory=list, description="Elements needed to improve score"
    )
    notes: Optional[str] = None

    @property
    def is_fully_developed(self) -> bool:
        """Check if criterion meets 'Fully Developed' standard."""
        return self.status == RubricStatus.FULLY_DEVELOPED and self.score >= 2

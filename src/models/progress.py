"""Progress tracking data models."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Priority level for action items."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionItemStatus(str, Enum):
    """Status of an action item."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class ActionItem(BaseModel):
    """Represents a specific action item to improve the notebook."""

    id: str
    title: str
    description: str
    priority: Priority
    status: ActionItemStatus = ActionItemStatus.TODO
    rubric_criterion: Optional[str] = Field(
        None, description="Related EN criterion"
    )
    estimated_pages: Optional[int] = Field(
        None, description="Estimated pages needed"
    )
    assigned_to: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    notes: str = ""


class ProgressSnapshot(BaseModel):
    """Snapshot of notebook progress at a point in time."""

    timestamp: datetime = Field(default_factory=datetime.now)
    total_pages: int
    rubric_scores: Dict[str, int] = Field(
        default_factory=dict, description="EN1-EN10 scores"
    )
    action_items: List[ActionItem] = Field(default_factory=list)
    completion_percentage: float = Field(
        ge=0.0, le=100.0, description="Overall completion %"
    )
    notes: str = ""

    def calculate_completion(self) -> float:
        """Calculate overall completion percentage based on rubric scores."""
        if not self.rubric_scores:
            return 0.0

        total_possible = len(self.rubric_scores) * 3  # Max 3 points per criterion
        total_earned = sum(self.rubric_scores.values())

        return (total_earned / total_possible) * 100 if total_possible > 0 else 0.0

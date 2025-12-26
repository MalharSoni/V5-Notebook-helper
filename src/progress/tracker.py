"""Track notebook progress over time."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..config import get_settings
from ..models import RubricScore
from ..models.progress import ProgressSnapshot, ActionItem


class ProgressTracker:
    """Tracks notebook progress over time."""

    def __init__(self, tracking_file: Optional[Path] = None):
        """
        Initialize progress tracker.

        Args:
            tracking_file: Path to tracking JSON file
        """
        settings = get_settings()
        self.tracking_file = tracking_file or settings.tracking_file
        self.snapshots: List[ProgressSnapshot] = []

        # Load existing snapshots if file exists
        if self.tracking_file.exists():
            self.load()

    def add_snapshot(
        self,
        total_pages: int,
        rubric_scores: Dict[str, RubricScore],
        action_items: List[ActionItem],
        notes: str = "",
    ) -> ProgressSnapshot:
        """
        Add a new progress snapshot.

        Args:
            total_pages: Total notebook pages
            rubric_scores: Current rubric scores
            action_items: Current action items
            notes: Optional notes about this snapshot

        Returns:
            Created ProgressSnapshot
        """
        # Convert rubric scores to simple dict
        scores_dict = {code: score.score for code, score in rubric_scores.items()}

        snapshot = ProgressSnapshot(
            total_pages=total_pages,
            rubric_scores=scores_dict,
            action_items=action_items,
            completion_percentage=0.0,  # Will be calculated
            notes=notes,
        )

        # Calculate completion percentage
        snapshot.completion_percentage = snapshot.calculate_completion()

        self.snapshots.append(snapshot)
        self.save()

        return snapshot

    def get_latest_snapshot(self) -> Optional[ProgressSnapshot]:
        """Get the most recent progress snapshot."""
        if not self.snapshots:
            return None
        return max(self.snapshots, key=lambda s: s.timestamp)

    def get_progress_history(self) -> List[ProgressSnapshot]:
        """Get all progress snapshots sorted by time."""
        return sorted(self.snapshots, key=lambda s: s.timestamp)

    def calculate_trend(self) -> Dict[str, float]:
        """
        Calculate progress trend.

        Returns:
            Dict with trend data
        """
        if len(self.snapshots) < 2:
            return {"trend": "insufficient_data", "change": 0.0}

        # Get first and last snapshots
        snapshots_sorted = self.get_progress_history()
        first = snapshots_sorted[0]
        last = snapshots_sorted[-1]

        # Calculate change in completion percentage
        change = last.completion_percentage - first.completion_percentage

        # Determine trend
        if change > 10:
            trend = "improving_fast"
        elif change > 5:
            trend = "improving"
        elif change > -5:
            trend = "stable"
        else:
            trend = "declining"

        return {
            "trend": trend,
            "change": change,
            "first_date": first.timestamp.isoformat(),
            "last_date": last.timestamp.isoformat(),
        }

    def save(self) -> None:
        """Save snapshots to file."""
        data = [
            {
                "timestamp": s.timestamp.isoformat(),
                "total_pages": s.total_pages,
                "rubric_scores": s.rubric_scores,
                "action_items": [ai.model_dump() for ai in s.action_items],
                "completion_percentage": s.completion_percentage,
                "notes": s.notes,
            }
            for s in self.snapshots
        ]

        with open(self.tracking_file, "w") as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        """Load snapshots from file."""
        with open(self.tracking_file, "r") as f:
            data = json.load(f)

        self.snapshots = []
        for item in data:
            # Convert action items
            action_items = [ActionItem(**ai) for ai in item.get("action_items", [])]

            snapshot = ProgressSnapshot(
                timestamp=datetime.fromisoformat(item["timestamp"]),
                total_pages=item["total_pages"],
                rubric_scores=item["rubric_scores"],
                action_items=action_items,
                completion_percentage=item["completion_percentage"],
                notes=item.get("notes", ""),
            )
            self.snapshots.append(snapshot)

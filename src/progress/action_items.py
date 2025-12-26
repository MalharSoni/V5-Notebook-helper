"""Manage action items for notebook improvement."""

import json
from pathlib import Path
from typing import List, Optional
import uuid

from ..config import get_settings
from ..models.progress import ActionItem, ActionItemStatus, Priority


class ActionItemManager:
    """Manages action items for notebook improvement."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize action item manager.

        Args:
            data_dir: Data directory path
        """
        settings = get_settings()
        self.data_dir = data_dir or settings.results_dir
        self.action_items_file = self.data_dir / "action_items.json"
        self.action_items: List[ActionItem] = []

        if self.action_items_file.exists():
            self.load()

    def create_from_gaps(self, gaps: List[Dict]) -> List[ActionItem]:
        """
        Create action items from identified gaps.

        Args:
            gaps: List of gap dictionaries

        Returns:
            List of created ActionItems
        """
        new_items = []

        for gap in gaps:
            item = ActionItem(
                id=str(uuid.uuid4()),
                title=gap["title"],
                description=gap["description"],
                priority=gap["priority"],
                rubric_criterion=gap.get("criterion"),
                notes=f"Current score: {gap.get('current_score', 'N/A')}",
            )
            new_items.append(item)
            self.action_items.append(item)

        self.save()
        return new_items

    def get_by_priority(self, priority: Priority) -> List[ActionItem]:
        """Get action items by priority."""
        return [item for item in self.action_items if item.priority == priority]

    def get_by_status(self, status: ActionItemStatus) -> List[ActionItem]:
        """Get action items by status."""
        return [item for item in self.action_items if item.status == status]

    def update_status(
        self, item_id: str, new_status: ActionItemStatus
    ) -> Optional[ActionItem]:
        """
        Update action item status.

        Args:
            item_id: Action item ID
            new_status: New status

        Returns:
            Updated ActionItem or None if not found
        """
        for item in self.action_items:
            if item.id == item_id:
                item.status = new_status
                if new_status == ActionItemStatus.COMPLETED:
                    from datetime import datetime

                    item.completed_at = datetime.now()
                self.save()
                return item
        return None

    def get_active_items(self) -> List[ActionItem]:
        """Get all active (not completed) action items."""
        return [
            item
            for item in self.action_items
            if item.status != ActionItemStatus.COMPLETED
        ]

    def save(self) -> None:
        """Save action items to file."""
        data = [item.model_dump() for item in self.action_items]

        with open(self.action_items_file, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def load(self) -> None:
        """Load action items from file."""
        with open(self.action_items_file, "r") as f:
            data = json.load(f)

        self.action_items = [ActionItem(**item) for item in data]

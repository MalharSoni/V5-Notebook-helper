"""Question bank for interview preparation."""

import random
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from ..config import get_settings


class QuestionBank:
    """Manages interview questions from YAML file."""

    def __init__(self, questions_file: Optional[Path] = None):
        """
        Initialize question bank.

        Args:
            questions_file: Path to questions YAML file
        """
        settings = get_settings()
        self.questions_file = questions_file or settings.questions_file
        self.questions = self._load_questions()

    def _load_questions(self) -> Dict:
        """Load questions from YAML file."""
        with open(self.questions_file, "r") as f:
            return yaml.safe_load(f)

    def get_questions_by_criterion(self, criterion: str) -> List[Dict]:
        """
        Get questions for a specific rubric criterion.

        Args:
            criterion: Criterion key (e.g., 'EN4_brainstorming')

        Returns:
            List of question dictionaries
        """
        return self.questions.get("interview_questions", {}).get(criterion, [])

    def get_random_questions(self, count: int = 5) -> List[Dict]:
        """
        Get random questions from all categories.

        Args:
            count: Number of questions to return

        Returns:
            List of random question dictionaries
        """
        all_questions = []
        for category_questions in self.questions.get("interview_questions", {}).values():
            all_questions.extend(category_questions)

        return random.sample(all_questions, min(count, len(all_questions)))

    def get_questions_for_gaps(self, gap_criteria: List[str]) -> List[Dict]:
        """
        Get questions focused on specific gap areas.

        Args:
            gap_criteria: List of criterion codes with gaps (e.g., ['EN4', 'EN6'])

        Returns:
            List of relevant questions
        """
        questions = []

        # Map criterion codes to question categories
        criterion_map = {
            "EN1": "EN1_identify_challenge",
            "EN4": "EN4_brainstorming",
            "EN5": "EN5_build_documentation",
            "EN6": "EN6_testing",
            "EN7": "EN7_iterations",
            "EN8": "EN8_project_management",
        }

        for criterion in gap_criteria:
            category = criterion_map.get(criterion)
            if category:
                category_questions = self.get_questions_by_criterion(category)
                questions.extend(category_questions)

        return questions

    def get_student_tips(self) -> Dict:
        """Get interview tips for students."""
        return self.questions.get("student_tips", {})

    def get_question_strategies(self) -> Dict:
        """Get question selection strategies."""
        return self.questions.get("question_strategies", {})

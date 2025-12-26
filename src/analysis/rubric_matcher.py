"""Match page analyses to rubric criteria and generate scores."""

from pathlib import Path
from typing import Dict, List

import yaml

from ..config import get_settings
from ..models import PageAnalysis, RubricCriterion, RubricScore, RubricStatus


class RubricMatcher:
    """Maps page analyses to rubric criteria and calculates scores."""

    def __init__(self, rubric_file: Path = None):
        """
        Initialize rubric matcher.

        Args:
            rubric_file: Path to rubric YAML file. If None, uses config default.
        """
        settings = get_settings()
        self.rubric_file = rubric_file or settings.rubric_file
        self.criteria = self._load_criteria()

    def _load_criteria(self) -> Dict[str, RubricCriterion]:
        """Load rubric criteria from YAML file."""
        with open(self.rubric_file, "r") as f:
            data = yaml.safe_load(f)

        criteria = {}
        for code, criterion_data in data["rubric_criteria"].items():
            criteria[code] = RubricCriterion(**criterion_data)

        return criteria

    def score_notebook(
        self, page_analyses: List[PageAnalysis]
    ) -> Dict[str, RubricScore]:
        """
        Score the entire notebook against all rubric criteria.

        Args:
            page_analyses: List of PageAnalysis from all pages

        Returns:
            Dict mapping criterion code to RubricScore
        """
        scores = {}

        # Score each criterion
        for code, criterion in self.criteria.items():
            score = self._score_criterion(code, criterion, page_analyses)
            scores[code] = score

        return scores

    def _score_criterion(
        self,
        code: str,
        criterion: RubricCriterion,
        page_analyses: List[PageAnalysis],
    ) -> RubricScore:
        """
        Score a single rubric criterion based on page analyses.

        Args:
            code: Criterion code (EN1, EN2, etc.)
            criterion: RubricCriterion object
            page_analyses: All page analyses

        Returns:
            RubricScore for this criterion
        """
        # Find pages relevant to this criterion
        relevant_pages = [
            p for p in page_analyses if code in p.rubric_categories
        ]

        # Aggregate key elements
        key_elements_found = self._aggregate_key_elements(relevant_pages)

        # Calculate score based on criterion
        score, status, evidence, missing = self._calculate_score(
            code, criterion, key_elements_found, relevant_pages
        )

        return RubricScore(
            criterion_code=code,
            status=status,
            score=score,
            evidence=evidence,
            missing_elements=missing,
        )

    def _aggregate_key_elements(
        self, pages: List[PageAnalysis]
    ) -> Dict[str, int]:
        """
        Aggregate key elements found across pages.

        Args:
            pages: List of PageAnalysis

        Returns:
            Dict of element name to count
        """
        elements = {}

        for page in pages:
            for element, found in page.key_elements.items():
                if found:
                    elements[element] = elements.get(element, 0) + 1

        return elements

    def _calculate_score(
        self,
        code: str,
        criterion: RubricCriterion,
        key_elements: Dict[str, int],
        relevant_pages: List[PageAnalysis],
    ) -> tuple:
        """
        Calculate score for a criterion.

        Args:
            code: Criterion code
            criterion: RubricCriterion
            key_elements: Aggregated key elements
            relevant_pages: Relevant pages

        Returns:
            Tuple of (score, status, evidence, missing_elements)
        """
        evidence = []
        missing = []

        # EN1: Identify the Challenge
        if code == "EN1":
            has_game_analysis = any(
                "game_analysis" in p.content_type.lower() for p in relevant_pages
            )
            has_challenge_id = len(relevant_pages) > 0

            if has_game_analysis and has_challenge_id:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [f"Found {len(relevant_pages)} pages identifying challenges"]
            elif has_challenge_id:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = ["Some challenge identification present"]
                missing = ["Need detailed game analysis with strategy breakdown"]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                missing = ["Missing challenge identification pages"]

        # EN4: Brainstorm Solutions (3+ options)
        elif code == "EN4":
            brainstorming_count = key_elements.get("brainstorming", 0)
            decision_matrix_count = key_elements.get("decision_matrix", 0)

            if brainstorming_count >= 3 and decision_matrix_count >= 1:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [
                    f"Found {brainstorming_count} pages with multiple design options",
                    f"Found {decision_matrix_count} decision matrices",
                ]
            elif brainstorming_count >= 1:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = [f"Found {brainstorming_count} brainstorming pages"]
                missing = [
                    "Need 3+ design options per subsystem with diagrams",
                    "Need decision matrices to justify selections",
                ]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                missing = [
                    "Missing brainstorming pages",
                    "Need 3+ options per subsystem",
                    "Need decision matrices",
                ]

        # EN5: Build and Program Documentation
        elif code == "EN5":
            cad_count = key_elements.get("cad_drawings", 0)
            build_pages = sum(
                1 for p in relevant_pages if "build" in p.content_type.lower()
            )

            if cad_count >= 3 and build_pages >= 5:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [
                    f"Found {cad_count} pages with CAD drawings",
                    f"Found {build_pages} build documentation pages",
                ]
            elif cad_count >= 1 or build_pages >= 2:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = ["Some build documentation present"]
                missing = ["Need more detailed build steps", "Add more CAD/technical drawings"]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                missing = ["Missing comprehensive build documentation"]

        # EN6: Test and Record Results
        elif code == "EN6":
            testing_count = key_elements.get("testing_data", 0)
            failure_docs = key_elements.get("failure_documentation", 0)

            if testing_count >= 3 and failure_docs >= 1:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [
                    f"Found {testing_count} pages with quantitative test data",
                    "Documented failures and successes",
                ]
            elif testing_count >= 1:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = ["Some testing documentation present"]
                missing = [
                    "Need more quantitative test data",
                    "Document both successes AND failures",
                ]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                missing = ["Missing testing documentation with quantitative data"]

        # EN7: Design Iterations
        elif code == "EN7":
            iteration_count = key_elements.get("design_iteration", 0)

            if iteration_count >= 3:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [f"Found {iteration_count} clear design iterations"]
            elif iteration_count >= 1:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = ["Some design iterations present"]
                missing = [
                    "Need more clearly labeled design cycles",
                    "Show progression and improvement over time",
                ]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                missing = ["Missing clear design iteration documentation"]

        # EN8: Project Management
        elif code == "EN8":
            meeting_count = key_elements.get("meeting_notes", 0)

            if meeting_count >= 5 and len(relevant_pages) >= 8:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [
                    f"Found {meeting_count} meeting notes",
                    "Project management documentation present",
                ]
            elif meeting_count >= 2:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = ["Some project management documentation"]
                missing = [
                    "Need more regular meeting notes",
                    "Document team roles and responsibilities",
                ]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                missing = ["Missing project management documentation"]

        # EN9: Sequential Documentation
        elif code == "EN9":
            dated_count = key_elements.get("dates_timestamps", 0)
            total_pages = len(relevant_pages) if relevant_pages else 1

            dated_percentage = (dated_count / total_pages) * 100 if total_pages > 0 else 0

            if dated_percentage >= 80:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [f"{dated_percentage:.0f}% of pages have dates/timestamps"]
            elif dated_percentage >= 50:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = [f"{dated_percentage:.0f}% of pages have dates"]
                missing = ["Add dates/timestamps to more entries"]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                missing = ["Most pages missing dates/timestamps"]

        # Default scoring for other criteria
        else:
            if len(relevant_pages) >= 5:
                score = 3
                status = RubricStatus.FULLY_DEVELOPED
                evidence = [f"Found {len(relevant_pages)} relevant pages"]
            elif len(relevant_pages) >= 2:
                score = 2
                status = RubricStatus.DEVELOPING
                evidence = [f"Found {len(relevant_pages)} relevant pages"]
            else:
                score = 1
                status = RubricStatus.PARTIAL
                evidence = []
                missing = [f"Need more content for {criterion.title}"]

        return score, status, evidence, missing

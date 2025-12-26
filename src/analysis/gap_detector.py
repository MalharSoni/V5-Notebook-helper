"""Detect gaps and missing elements in engineering notebook."""

from typing import Dict, List, Tuple

from ..models import PageAnalysis, RubricScore, RubricStatus
from ..models.progress import Priority


class GapDetector:
    """Identifies missing elements and gaps in notebook documentation."""

    def detect_gaps(
        self, rubric_scores: Dict[str, RubricScore], page_analyses: List[PageAnalysis]
    ) -> List[Dict]:
        """
        Detect gaps in the notebook.

        Args:
            rubric_scores: Dict of criterion codes to RubricScores
            page_analyses: List of all PageAnalysis

        Returns:
            List of gap dictionaries with title, description, priority, criterion
        """
        gaps = []

        # Check each criterion's missing elements
        for code, score in rubric_scores.items():
            for missing in score.missing_elements:
                priority = self._determine_priority(code, score)

                gaps.append(
                    {
                        "title": f"{code}: {missing}",
                        "description": self._get_gap_description(code, missing),
                        "priority": priority,
                        "criterion": code,
                        "current_score": score.score,
                    }
                )

        # Check for specific critical gaps
        critical_gaps = self._check_critical_gaps(rubric_scores, page_analyses)
        gaps.extend(critical_gaps)

        # Sort by priority
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        gaps.sort(key=lambda x: priority_order.get(x["priority"], 3))

        return gaps

    def _determine_priority(self, criterion_code: str, score: RubricScore) -> Priority:
        """
        Determine priority level for a gap.

        Args:
            criterion_code: EN criterion code
            score: Current RubricScore

        Returns:
            Priority level
        """
        # High priority for EN1-EN4 (required for Fully Developed status)
        if criterion_code in ["EN1", "EN2", "EN3", "EN4"] and score.score < 2:
            return Priority.HIGH

        # High priority for very low scores
        if score.score == 0:
            return Priority.HIGH

        # Medium priority for scores of 1-2
        if score.score <= 2:
            return Priority.MEDIUM

        # Low priority for scores of 3+
        return Priority.LOW

    def _get_gap_description(self, criterion_code: str, missing: str) -> str:
        """
        Get detailed description for a gap.

        Args:
            criterion_code: EN criterion code
            missing: Missing element description

        Returns:
            Detailed description of what to add
        """
        descriptions = {
            "EN1": "Add detailed game and challenge analysis at the start of design cycles. Use both text and diagrams.",
            "EN4": "Document 3+ design options for each subsystem with labeled diagrams. Include decision matrix to show selection process.",
            "EN5": "Add comprehensive build documentation with CAD, technical drawings, and enough detail to recreate the robot.",
            "EN6": "Document testing procedures with quantitative data. Include both successes AND failures.",
            "EN7": "Clearly label design cycles and show progression/improvement over multiple iterations.",
            "EN8": "Add team roles, meeting notes with dates/decisions, and budget/resource tracking.",
            "EN9": "Ensure all entries have dates, timestamps, and contributor names.",
        }

        base_description = descriptions.get(criterion_code, "Address this gap in your notebook.")
        return f"{base_description} Specifically: {missing}"

    def _check_critical_gaps(
        self, rubric_scores: Dict[str, RubricScore], page_analyses: List[PageAnalysis]
    ) -> List[Dict]:
        """
        Check for critical gaps that might not be captured by rubric scoring.

        Args:
            rubric_scores: Current rubric scores
            page_analyses: All page analyses

        Returns:
            List of critical gap dictionaries
        """
        critical_gaps = []

        # Check for Fully Developed status
        en1_4_scores = [rubric_scores.get(f"EN{i}", RubricScore(
            criterion_code=f"EN{i}", status=RubricStatus.MISSING, score=0, evidence=[], missing_elements=[]
        )).score for i in range(1, 5)]

        if any(score < 2 for score in en1_4_scores):
            critical_gaps.append(
                {
                    "title": "Fully Developed Status At Risk",
                    "description": "Notebook needs 2+ points in EN1-EN4 to be considered 'Fully Developed'. This is REQUIRED for Excellence/Design/Innovate awards.",
                    "priority": Priority.HIGH,
                    "criterion": "OVERALL",
                    "current_score": min(en1_4_scores),
                }
            )

        # Check for missing brainstorming (common critical gap)
        en4_score = rubric_scores.get("EN4", RubricScore(
            criterion_code="EN4", status=RubricStatus.MISSING, score=0, evidence=[], missing_elements=[]
        ))
        if en4_score.score < 2:
            critical_gaps.append(
                {
                    "title": "Critical: Missing 3+ Design Options",
                    "description": "Must show 3+ possible solutions for EACH major subsystem (intake, drivetrain, etc.) with labeled diagrams. This is a core requirement judges look for.",
                    "priority": Priority.HIGH,
                    "criterion": "EN4",
                    "current_score": en4_score.score,
                }
            )

        # Check for missing decision matrices
        has_decision_matrix = any(
            p.key_elements.get("decision_matrix", False) for p in page_analyses
        )
        if not has_decision_matrix:
            critical_gaps.append(
                {
                    "title": "Critical: Missing Decision Matrices",
                    "description": "Need decision matrices to justify design selections. Include weighted criteria (speed, reliability, ease of build, etc.) with scoring.",
                    "priority": Priority.HIGH,
                    "criterion": "EN4",
                    "current_score": en4_score.score,
                }
            )

        # Check for missing testing data
        testing_pages = sum(
            1 for p in page_analyses if p.key_elements.get("testing_data", False)
        )
        if testing_pages < 2:
            critical_gaps.append(
                {
                    "title": "Missing Quantitative Testing Data",
                    "description": "Need quantitative test results (numbers, measurements, success rates). Not just 'it worked well' but '15 rings in 30 seconds with 90% success rate'.",
                    "priority": Priority.MEDIUM,
                    "criterion": "EN6",
                    "current_score": rubric_scores.get("EN6", RubricScore(
                        criterion_code="EN6", status=RubricStatus.MISSING, score=0, evidence=[], missing_elements=[]
                    )).score,
                }
            )

        # Check for design iteration labeling
        iteration_pages = sum(
            1 for p in page_analyses if p.key_elements.get("design_iteration", False)
        )
        if iteration_pages < 2:
            critical_gaps.append(
                {
                    "title": "Unclear Design Cycle Labeling",
                    "description": "Design cycles should be clearly labeled (Design Cycle 1, Design Cycle 2, etc.) to show progression and iteration.",
                    "priority": Priority.HIGH,
                    "criterion": "EN7",
                    "current_score": rubric_scores.get("EN7", RubricScore(
                        criterion_code="EN7", status=RubricStatus.MISSING, score=0, evidence=[], missing_elements=[]
                    )).score,
                }
            )

        return critical_gaps

    def get_recommendations(
        self, rubric_scores: Dict[str, RubricScore], gaps: List[Dict]
    ) -> List[str]:
        """
        Generate prioritized recommendations based on gaps.

        Args:
            rubric_scores: Current rubric scores
            gaps: List of identified gaps

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # High priority recommendations
        high_priority_gaps = [g for g in gaps if g["priority"] == Priority.HIGH]
        if high_priority_gaps:
            recommendations.append(
                f"URGENT: Address {len(high_priority_gaps)} high-priority gaps to achieve Fully Developed status"
            )

        # Specific recommendations for Excellence Award
        en_scores = {code: score.score for code, score in rubric_scores.items()}
        avg_score = sum(en_scores.values()) / len(en_scores) if en_scores else 0

        if avg_score < 2.5:
            recommendations.append(
                "Target: Bring average rubric score to 2.5+ for Excellence Award competitiveness"
            )

        # Recommendations based on specific gaps
        if any("brainstorm" in g["title"].lower() for g in gaps):
            recommendations.append(
                "Add brainstorming sections showing 3+ options per subsystem with labeled diagrams"
            )

        if any("decision matrix" in g["title"].lower() for g in gaps):
            recommendations.append(
                "Create decision matrices for major design decisions (weighted criteria: speed, reliability, ease of build, cost)"
            )

        if any("iteration" in g["title"].lower() for g in gaps):
            recommendations.append(
                "Clearly label design cycles and show progression (Design Cycle 1 → 2 → 3)"
            )

        if any("testing" in g["title"].lower() for g in gaps):
            recommendations.append(
                "Add quantitative testing data with measurements, success rates, and comparison data"
            )

        # General improvement recommendation
        if avg_score >= 2.5:
            recommendations.append(
                "Good progress! Focus on excellence in top priority areas and adding depth to existing documentation"
            )

        return recommendations

"""Generate analysis reports in various formats."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from ..models import NotebookAnalysis, PageAnalysis, RubricScore, RubricStatus


class ReportGenerator:
    """Generates formatted reports from notebook analysis."""

    def __init__(self):
        """Initialize report generator."""
        self.console = Console()

    def generate_terminal_report(
        self,
        rubric_scores: Dict[str, RubricScore],
        gaps: List[Dict],
        recommendations: List[str],
    ) -> None:
        """
        Generate and print terminal report using Rich.

        Args:
            rubric_scores: Dict of criterion codes to scores
            gaps: List of gap dictionaries
            recommendations: List of recommendations
        """
        # Header
        self.console.print("\n")
        self.console.print(
            Panel.fit(
                "[bold blue]VEX Engineering Notebook Analysis Report[/bold blue]",
                border_style="blue",
            )
        )

        # Rubric Scores Table
        self._print_rubric_table(rubric_scores)

        # Overall Status
        self._print_overall_status(rubric_scores)

        # Gaps and Missing Elements
        self._print_gaps(gaps)

        # Recommendations
        self._print_recommendations(recommendations)

    def _print_rubric_table(self, rubric_scores: Dict[str, RubricScore]) -> None:
        """Print rubric scores in a table."""
        table = Table(title="Rubric Scores (EN1-EN10)", show_header=True)

        table.add_column("Criterion", style="cyan")
        table.add_column("Score", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Evidence Count", justify="center")

        for code in sorted(rubric_scores.keys()):
            score = rubric_scores[code]

            # Color code by score
            if score.score >= 3:
                score_color = "green"
            elif score.score >= 2:
                score_color = "yellow"
            else:
                score_color = "red"

            # Status color
            if score.status == RubricStatus.FULLY_DEVELOPED:
                status_color = "green"
            elif score.status == RubricStatus.DEVELOPING:
                status_color = "yellow"
            else:
                status_color = "red"

            table.add_row(
                code,
                f"[{score_color}]{score.score}/3[/{score_color}]",
                f"[{status_color}]{score.status.value}[/{status_color}]",
                str(len(score.evidence)),
            )

        self.console.print("\n", table)

    def _print_overall_status(self, rubric_scores: Dict[str, RubricScore]) -> None:
        """Print overall notebook status."""
        # Check Fully Developed status
        en1_4_scores = [
            rubric_scores.get(f"EN{i}").score for i in range(1, 5)
            if f"EN{i}" in rubric_scores
        ]
        fully_developed = all(score >= 2 for score in en1_4_scores)

        # Calculate average score
        scores = [s.score for s in rubric_scores.values()]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Determine color
        status_color = "green" if fully_developed else "red"

        status_text = Text()
        status_text.append("\nOverall Status:\n", style="bold")
        status_text.append(
            f"  Fully Developed: {fully_developed}\n",
            style=f"bold {status_color}",
        )
        status_text.append(
            f"  Average Score: {avg_score:.2f}/3.0\n",
            style="bold",
        )
        status_text.append(
            f"  Excellence Award Ready: {fully_developed and avg_score >= 2.5}\n",
            style=f"bold {'green' if (fully_developed and avg_score >= 2.5) else 'red'}",
        )

        self.console.print(status_text)

    def _print_gaps(self, gaps: List[Dict]) -> None:
        """Print identified gaps."""
        if not gaps:
            self.console.print("\n[green]No significant gaps identified![/green]")
            return

        table = Table(title="\nIdentified Gaps", show_header=True)
        table.add_column("Priority", style="bold")
        table.add_column("Gap", style="cyan", no_wrap=False)
        table.add_column("Criterion", justify="center")

        for gap in gaps[:10]:  # Show top 10
            priority = gap["priority"]
            priority_color = {
                "high": "red",
                "medium": "yellow",
                "low": "blue",
            }.get(priority.lower(), "white")

            table.add_row(
                f"[{priority_color}]{priority.upper()}[/{priority_color}]",
                gap["title"],
                gap["criterion"],
            )

        self.console.print(table)

        if len(gaps) > 10:
            self.console.print(
                f"\n[dim]... and {len(gaps) - 10} more gaps[/dim]"
            )

    def _print_recommendations(self, recommendations: List[str]) -> None:
        """Print recommendations."""
        if not recommendations:
            return

        self.console.print("\n[bold]Recommendations:[/bold]")
        for i, rec in enumerate(recommendations, 1):
            self.console.print(f"  {i}. {rec}")

    def generate_markdown_report(
        self,
        rubric_scores: Dict[str, RubricScore],
        gaps: List[Dict],
        recommendations: List[str],
        output_file: Path,
    ) -> None:
        """
        Generate markdown report and save to file.

        Args:
            rubric_scores: Rubric scores
            gaps: Identified gaps
            recommendations: Recommendations
            output_file: Output file path
        """
        lines = []

        # Header
        lines.append("# VEX Engineering Notebook Analysis Report\n")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("---\n\n")

        # Rubric Scores
        lines.append("## Rubric Scores\n\n")
        lines.append("| Criterion | Score | Status | Evidence |\n")
        lines.append("|-----------|-------|--------|----------|\n")

        for code in sorted(rubric_scores.keys()):
            score = rubric_scores[code]
            evidence_count = len(score.evidence)

            lines.append(
                f"| {code} | {score.score}/3 | {score.status.value} | {evidence_count} items |\n"
            )

        # Overall Status
        en1_4_scores = [
            rubric_scores.get(f"EN{i}").score for i in range(1, 5)
            if f"EN{i}" in rubric_scores
        ]
        fully_developed = all(score >= 2 for score in en1_4_scores)
        avg_score = sum(s.score for s in rubric_scores.values()) / len(rubric_scores)

        lines.append("\n## Overall Status\n\n")
        lines.append(f"- **Fully Developed:** {fully_developed}\n")
        lines.append(f"- **Average Score:** {avg_score:.2f}/3.0\n")
        lines.append(
            f"- **Excellence Award Ready:** {fully_developed and avg_score >= 2.5}\n\n"
        )

        # Gaps
        if gaps:
            lines.append("## Identified Gaps\n\n")
            for gap in gaps:
                lines.append(f"### {gap['title']}\n\n")
                lines.append(f"- **Priority:** {gap['priority']}\n")
                lines.append(f"- **Criterion:** {gap['criterion']}\n")
                lines.append(f"- **Description:** {gap['description']}\n\n")

        # Recommendations
        if recommendations:
            lines.append("## Recommendations\n\n")
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}\n")

        # Write to file
        output_file.write_text("".join(lines))

    def generate_json_report(
        self,
        notebook_analysis: NotebookAnalysis,
        output_file: Path,
    ) -> None:
        """
        Generate JSON report.

        Args:
            notebook_analysis: Complete NotebookAnalysis object
            output_file: Output file path
        """
        notebook_analysis.save_to_file(output_file)

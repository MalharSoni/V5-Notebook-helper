"""Interactive practice interview session."""

from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .question_bank import QuestionBank


class PracticeSession:
    """Run interactive practice interview sessions."""

    def __init__(self, question_bank: Optional[QuestionBank] = None):
        """
        Initialize practice session.

        Args:
            question_bank: QuestionBank instance
        """
        self.question_bank = question_bank or QuestionBank()
        self.console = Console()

    def run_random_session(self, num_questions: int = 5) -> None:
        """
        Run practice session with random questions.

        Args:
            num_questions: Number of questions to ask
        """
        self.console.print("\n")
        self.console.print(
            Panel.fit(
                "[bold blue]VEX Interview Practice Session[/bold blue]",
                subtitle="Random Questions",
                border_style="blue",
            )
        )

        questions = self.question_bank.get_random_questions(num_questions)

        for i, q_data in enumerate(questions, 1):
            self._ask_question(i, num_questions, q_data)

        self._show_tips()

    def run_focused_session(self, criteria: List[str]) -> None:
        """
        Run practice session focused on specific criteria.

        Args:
            criteria: List of criterion codes to focus on
        """
        self.console.print("\n")
        self.console.print(
            Panel.fit(
                "[bold blue]VEX Interview Practice Session[/bold blue]",
                subtitle=f"Focused on: {', '.join(criteria)}",
                border_style="blue",
            )
        )

        questions = self.question_bank.get_questions_for_gaps(criteria)

        if not questions:
            self.console.print(
                "[yellow]No questions found for specified criteria.[/yellow]"
            )
            return

        for i, q_data in enumerate(questions, 1):
            self._ask_question(i, len(questions), q_data)

        self._show_tips()

    def _ask_question(
        self, question_num: int, total: int, q_data: dict
    ) -> None:
        """
        Ask a single question and provide follow-ups.

        Args:
            question_num: Current question number
            total: Total number of questions
            q_data: Question data dictionary
        """
        self.console.print(f"\n[bold]Question {question_num}/{total}:[/bold]")
        self.console.print(f"[cyan]{q_data['question']}[/cyan]\n")

        # Wait for user to be ready
        Prompt.ask("Press Enter when ready for follow-ups", default="")

        # Show follow-ups if available
        follow_ups = q_data.get("follow_ups", [])
        if follow_ups:
            self.console.print("\n[bold]Follow-up questions:[/bold]")
            for i, follow_up in enumerate(follow_ups, 1):
                self.console.print(f"  {i}. {follow_up}")

        self.console.print("\n" + "-" * 60)

        # Pause before next question
        if question_num < total:
            Prompt.ask("\nPress Enter for next question", default="")

    def _show_tips(self) -> None:
        """Show interview tips to students."""
        tips = self.question_bank.get_student_tips()

        self.console.print("\n")
        self.console.print(
            Panel.fit(
                "[bold green]Interview Tips[/bold green]",
                border_style="green",
            )
        )

        if "during_interview" in tips:
            self.console.print("\n[bold]During the Interview:[/bold]")
            for tip in tips["during_interview"]:
                self.console.print(f"  • {tip}")

        if "common_mistakes" in tips:
            self.console.print("\n[bold]Common Mistakes to Avoid:[/bold]")
            for mistake in tips["common_mistakes"]:
                self.console.print(f"  • {mistake}")

    def show_all_tips(self) -> None:
        """Display all interview tips."""
        tips = self.question_bank.get_student_tips()

        self.console.print("\n")
        self.console.print(
            Panel.fit(
                "[bold blue]Complete Interview Guide[/bold blue]",
                border_style="blue",
            )
        )

        for category, items in tips.items():
            self.console.print(f"\n[bold]{category.replace('_', ' ').title()}:[/bold]")
            for item in items:
                self.console.print(f"  • {item}")

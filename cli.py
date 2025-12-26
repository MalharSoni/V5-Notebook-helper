#!/usr/bin/env python3
"""CLI for V5-Notebook-Helper toolkit."""

import sys
import random
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import get_settings
from src.analysis import VisionAnalyzer, RubricMatcher, GapDetector, ReportGenerator
from src.progress import ProgressTracker, ActionItemManager
from src.interview import QuestionBank, PracticeSession
from src.models import NotebookAnalysis, NotebookPage
from src.generation import ContentGenerator, BrainstormGenerator, TestingDataGenerator, MeetingNotesGenerator

app = typer.Typer(
    name="notebook-helper",
    help="VEX Engineering Notebook Analysis Toolkit for Team 839Z",
)
console = Console()


@app.command()
def analyze(
    pages: str = typer.Option(
        "all",
        help="Pages to analyze: 'all' or range like '1-10'",
    ),
    save: bool = typer.Option(
        True,
        help="Save analysis results",
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        help="Verbose output",
    ),
):
    """Analyze notebook pages using GPT-4 Vision."""
    settings = get_settings()
    console.print("\n[bold blue]V5-Notebook-Helper: Notebook Analysis[/bold blue]\n")

    # Check if notebook directory exists
    if not settings.notebook_pages_dir.exists():
        console.print(
            f"[red]Error: Notebook directory not found: {settings.notebook_pages_dir}[/red]"
        )
        console.print("Please ensure notebook-pages/ directory exists with PNG images.")
        raise typer.Exit(1)

    # Find all pages
    page_files = sorted(settings.notebook_pages_dir.glob("page_*.png"))

    if not page_files:
        console.print(
            "[red]Error: No page_*.png files found in notebook-pages/[/red]"
        )
        raise typer.Exit(1)

    console.print(f"Found {len(page_files)} pages in notebook-pages/")

    # Parse page range
    if pages == "all":
        pages_to_analyze = page_files
    else:
        # Parse range (e.g., "1-10")
        try:
            start, end = map(int, pages.split("-"))
            pages_to_analyze = page_files[start - 1 : end]
        except:
            console.print(
                "[red]Error: Invalid page range. Use 'all' or 'start-end' (e.g., '1-10')[/red]"
            )
            raise typer.Exit(1)

    console.print(f"Analyzing {len(pages_to_analyze)} pages...")

    # Initialize analyzer
    try:
        analyzer = VisionAnalyzer()
    except Exception as e:
        console.print(f"[red]Error initializing analyzer: {e}[/red]")
        console.print("\nMake sure OPENAI_API_KEY is set in .env file")
        raise typer.Exit(1)

    # Create NotebookPage objects
    notebook_pages = [
        NotebookPage(page_number=i, file_path=f)
        for i, f in enumerate(pages_to_analyze, 1)
    ]

    # Analyze pages with progress bar
    page_analyses = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing pages...", total=len(notebook_pages))

        for page in notebook_pages:
            if verbose:
                console.print(f"  Analyzing page {page.page_number}...")

            analysis = analyzer.analyze_page(page)
            page_analyses.append(analysis)
            progress.update(task, advance=1)

    console.print(f"[green]✓ Analyzed {len(page_analyses)} pages[/green]")

    # Score against rubric
    console.print("\nScoring against rubric...")
    matcher = RubricMatcher()
    rubric_scores = matcher.score_notebook(page_analyses)

    # Detect gaps
    console.print("Detecting gaps...")
    detector = GapDetector()
    gaps = detector.detect_gaps(rubric_scores, page_analyses)
    recommendations = detector.get_recommendations(rubric_scores, gaps)

    # Create notebook analysis object
    notebook_analysis = NotebookAnalysis(
        total_pages=len(page_files),
        pages_analyzed=len(page_analyses),
        page_analyses=page_analyses,
        rubric_scores={code: score.model_dump() for code, score in rubric_scores.items()},
        gaps_identified=[g["title"] for g in gaps],
        recommendations=recommendations,
    )

    # Save if requested
    if save:
        output_file = settings.results_dir / "latest_analysis.json"
        notebook_analysis.save_to_file(output_file)
        console.print(f"\n[green]✓ Saved analysis to {output_file}[/green]")

    # Generate terminal report
    console.print("\n" + "=" * 60 + "\n")
    report_gen = ReportGenerator()
    report_gen.generate_terminal_report(rubric_scores, gaps, recommendations)

    console.print(f"\n[green]✓ Analysis complete![/green]")


@app.command()
def gaps():
    """View identified gaps in the notebook."""
    settings = get_settings()
    analysis_file = settings.results_dir / "latest_analysis.json"

    if not analysis_file.exists():
        console.print("[yellow]No analysis found. Run 'analyze' first.[/yellow]")
        raise typer.Exit(1)

    notebook_analysis = NotebookAnalysis.load_from_file(analysis_file)

    console.print("\n[bold blue]Identified Gaps[/bold blue]\n")

    for i, gap in enumerate(notebook_analysis.gaps_identified, 1):
        console.print(f"{i}. {gap}")

    console.print(f"\n[bold]Total gaps: {len(notebook_analysis.gaps_identified)}[/bold]")


@app.command()
def progress():
    """View progress tracking data."""
    tracker = ProgressTracker()
    latest = tracker.get_latest_snapshot()

    if not latest:
        console.print("[yellow]No progress data available.[/yellow]")
        raise typer.Exit(1)

    console.print("\n[bold blue]Notebook Progress[/bold blue]\n")
    console.print(f"Completion: {latest.completion_percentage:.1f}%")
    console.print(f"Total Pages: {latest.total_pages}")
    console.print(f"Last Updated: {latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    console.print("\n[bold]Rubric Scores:[/bold]")
    for criterion, score in sorted(latest.rubric_scores.items()):
        console.print(f"  {criterion}: {score}/3")


@app.command()
def interview(
    mode: str = typer.Argument(
        "practice",
        help="Mode: 'practice' or 'tips'",
    ),
    count: int = typer.Option(
        5,
        help="Number of questions for practice mode",
    ),
):
    """Practice interview questions or view tips."""
    question_bank = QuestionBank()
    practice_session = PracticeSession(question_bank)

    if mode == "practice":
        practice_session.run_random_session(count)
    elif mode == "tips":
        practice_session.show_all_tips()
    else:
        console.print(f"[red]Unknown mode: {mode}. Use 'practice' or 'tips'[/red]")
        raise typer.Exit(1)


@app.command()
def serve(
    host: str = typer.Option(
        "127.0.0.1",
        help="Host to bind to",
    ),
    port: int = typer.Option(
        8000,
        help="Port to bind to",
    ),
):
    """Start the web dashboard server."""
    import uvicorn
    from src.web.app import app as web_app

    console.print(f"\n[bold blue]Starting V5-Notebook-Helper Dashboard[/bold blue]\n")
    console.print(f"Server running at: http://{host}:{port}")
    console.print("Press Ctrl+C to stop\n")

    uvicorn.run(web_app, host=host, port=port)


@app.command()
def info():
    """Show project information."""
    console.print("\n[bold blue]V5-Notebook-Helper[/bold blue]")
    console.print("Engineering Notebook Analysis Toolkit\n")
    console.print("[bold]Team:[/bold] 839Z - Caution Tape ZOOM!")
    console.print("[bold]Season:[/bold] 2024-2025 VRC High Stakes")
    console.print("[bold]Goal:[/bold] Excellence Award\n")
    console.print("[bold]Features:[/bold]")
    console.print("  • GPT-4 Vision notebook analysis")
    console.print("  • EN1-EN10 rubric scoring")
    console.print("  • Gap detection and recommendations")
    console.print("  • Progress tracking")
    console.print("  • Interview practice")
    console.print("  • AI content generation")
    console.print("  • Web dashboard\n")


# ============================================================================
# CONTENT GENERATION COMMANDS
# ============================================================================

@app.command()
def generate_game_analysis(
    game: str = typer.Option("VRC High Stakes", help="Game name"),
    strategies: int = typer.Option(8, help="Number of strategies to analyze"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
):
    """Generate comprehensive game analysis section."""
    console.print("\n[bold blue]Generating Game Analysis[/bold blue]\n")

    generator = ContentGenerator()

    with console.status("[bold green]Generating content..."):
        content = generator.generate_game_analysis(game, strategies)

    if output:
        output.write_text(content)
        console.print(f"[green]✓ Saved to {output}[/green]")
    else:
        console.print(content)

    console.print(f"\n[green]✓ Generated game analysis with {strategies} strategies[/green]")


@app.command()
def generate_brainstorm(
    subsystem: str = typer.Argument(..., help="Subsystem to brainstorm (e.g., intake, drivetrain)"),
    options: int = typer.Option(4, help="Number of design options"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
):
    """Generate brainstorming section with multiple design options."""
    console.print(f"\n[bold blue]Generating Brainstorm for {subsystem}[/bold blue]\n")

    generator = BrainstormGenerator()

    with console.status("[bold green]Generating content..."):
        sections = generator.generate_complete_brainstorm_section(subsystem)

    # Combine all sections
    full_content = f"""# {subsystem.title()} Brainstorming

## Initial Analysis
{sections['initial_analysis']}

## Design Options
{sections['options']}

## Decision Matrix
{sections['decision_matrix']}

## Conclusion
{sections['conclusion']}
"""

    if output:
        output.write_text(full_content)
        console.print(f"[green]✓ Saved to {output}[/green]")
    else:
        console.print(full_content)

    console.print(f"\n[green]✓ Generated complete brainstorming section[/green]")


@app.command()
def generate_testing(
    subsystem: str = typer.Argument(..., help="What to test"),
    metric: str = typer.Option("performance", help="Test metric"),
    target: float = typer.Option(100.0, help="Target value"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
):
    """Generate testing documentation with realistic data."""
    console.print(f"\n[bold blue]Generating Testing Documentation[/bold blue]\n")

    generator = TestingDataGenerator()

    with console.status("[bold green]Generating content..."):
        content = generator.generate_performance_test(subsystem, metric, target)

    if output:
        output.write_text(content)
        console.print(f"[green]✓ Saved to {output}[/green]")
    else:
        console.print(content)

    console.print(f"\n[green]✓ Generated testing documentation with data[/green]")


@app.command()
def generate_meetings(
    count: int = typer.Option(15, help="Number of meetings to generate"),
    team_size: int = typer.Option(5, help="Team size"),
    output_dir: Optional[Path] = typer.Option(None, help="Output directory"),
):
    """Generate a season's worth of team meeting notes."""
    console.print(f"\n[bold blue]Generating {count} Meeting Notes[/bold blue]\n")

    generator = MeetingNotesGenerator()

    with console.status("[bold green]Generating meetings..."):
        meetings = generator.generate_season_meetings(count, team_size)

    if output_dir:
        output_dir.mkdir(exist_ok=True, parents=True)
        for i, meeting in enumerate(meetings, 1):
            file_path = output_dir / f"meeting_{i:02d}.md"
            file_path.write_text(meeting)
        console.print(f"[green]✓ Saved {len(meetings)} meetings to {output_dir}[/green]")
    else:
        # Print first meeting as sample
        console.print(meetings[0])
        console.print(f"\n[dim]... and {len(meetings) - 1} more meetings[/dim]")

    console.print(f"\n[green]✓ Generated {len(meetings)} meeting notes[/green]")


@app.command()
def generate_build_doc(
    component: str = typer.Argument(..., help="Component to document"),
    detail: str = typer.Option("high", help="Detail level: high, medium"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
):
    """Generate detailed build documentation."""
    console.print(f"\n[bold blue]Generating Build Documentation[/bold blue]\n")

    generator = ContentGenerator()

    with console.status("[bold green]Generating content..."):
        content = generator.generate_build_documentation(component, detail)

    if output:
        output.write_text(content)
        console.print(f"[green]✓ Saved to {output}[/green]")
    else:
        console.print(content)

    console.print(f"\n[green]✓ Generated build documentation[/green]")


@app.command()
def generate_iteration(
    subsystem: str = typer.Argument(..., help="Subsystem being iterated"),
    iteration: int = typer.Option(2, help="Iteration number"),
    issues: str = typer.Option("", help="Issues from previous iteration"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
):
    """Generate design iteration documentation."""
    console.print(f"\n[bold blue]Generating Design Iteration {iteration}[/bold blue]\n")

    generator = ContentGenerator()

    with console.status("[bold green]Generating content..."):
        content = generator.generate_design_iteration(subsystem, iteration, issues)

    if output:
        output.write_text(content)
        console.print(f"[green]✓ Saved to {output}[/green]")
    else:
        console.print(content)

    console.print(f"\n[green]✓ Generated iteration documentation[/green]")


@app.command()
def generate_full_notebook(
    output_dir: Path = typer.Argument(..., help="Output directory for generated content"),
    subsystems: str = typer.Option("intake,drivetrain,lift", help="Comma-separated subsystems"),
):
    """Generate a complete test notebook with all sections."""
    console.print("\n[bold blue]Generating Complete Test Notebook[/bold blue]\n")

    output_dir.mkdir(exist_ok=True, parents=True)
    subsystem_list = [s.strip() for s in subsystems.split(",")]

    console.print(f"Will generate content for subsystems: {', '.join(subsystem_list)}\n")

    generator = ContentGenerator()
    brainstorm_gen = BrainstormGenerator()
    testing_gen = TestingDataGenerator()
    meeting_gen = MeetingNotesGenerator()

    # 1. Game Analysis
    console.print("[yellow]1. Generating game analysis...[/yellow]")
    game_analysis = generator.generate_game_analysis()
    (output_dir / "01_game_analysis.md").write_text(game_analysis)

    # 2. Brainstorming for each subsystem
    console.print(f"[yellow]2. Generating brainstorming for {len(subsystem_list)} subsystems...[/yellow]")
    for i, subsystem in enumerate(subsystem_list, 1):
        sections = brainstorm_gen.generate_complete_brainstorm_section(subsystem)
        content = f"""# {subsystem.title()} Brainstorming

{sections['initial_analysis']}

{sections['options']}

{sections['decision_matrix']}

{sections['conclusion']}
"""
        (output_dir / f"02_{i}_brainstorm_{subsystem}.md").write_text(content)

    # 3. Build documentation
    console.print("[yellow]3. Generating build documentation...[/yellow]")
    for i, subsystem in enumerate(subsystem_list, 1):
        build_doc = generator.generate_build_documentation(subsystem)
        (output_dir / f"03_{i}_build_{subsystem}.md").write_text(build_doc)

    # 4. Testing documentation
    console.print("[yellow]4. Generating testing documentation...[/yellow]")
    for i, subsystem in enumerate(subsystem_list, 1):
        test_doc = testing_gen.generate_performance_test(
            subsystem,
            f"{subsystem} efficiency",
            random.uniform(80, 120)
        )
        (output_dir / f"04_{i}_testing_{subsystem}.md").write_text(test_doc)

    # 5. Design iterations
    console.print("[yellow]5. Generating design iterations...[/yellow]")
    for subsystem in subsystem_list[:2]:  # First 2 subsystems get iterations
        iteration2 = generator.generate_design_iteration(
            subsystem, 2, "Performance below target, friction issues"
        )
        (output_dir / f"05_iteration2_{subsystem}.md").write_text(iteration2)

    # 6. Meeting notes
    console.print("[yellow]6. Generating meeting notes (10 meetings)...[/yellow]")
    meetings = meeting_gen.generate_season_meetings(num_meetings=10, team_size=5)
    meetings_dir = output_dir / "meetings"
    meetings_dir.mkdir(exist_ok=True)
    for i, meeting in enumerate(meetings, 1):
        (meetings_dir / f"meeting_{i:02d}.md").write_text(meeting)

    # 7. Programming documentation
    console.print("[yellow]7. Generating programming documentation...[/yellow]")
    prog_doc = generator.generate_programming_documentation("autonomous routine")
    (output_dir / "06_programming.md").write_text(prog_doc)

    console.print(f"\n[green]✓ Complete test notebook generated in {output_dir}[/green]")
    console.print("\n[bold]Generated files:[/bold]")
    console.print("  • Game analysis")
    console.print(f"  • Brainstorming for {len(subsystem_list)} subsystems")
    console.print(f"  • Build documentation for {len(subsystem_list)} subsystems")
    console.print(f"  • Testing documentation for {len(subsystem_list)} subsystems")
    console.print(f"  • Design iterations")
    console.print(f"  • 10 meeting notes")
    console.print(f"  • Programming documentation")


if __name__ == "__main__":
    app()

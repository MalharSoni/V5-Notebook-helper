"""Main content generator using GPT-4 to create notebook content."""

from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI

from ..config import get_settings


class ContentGenerator:
    """Generate notebook content using AI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize content generator."""
        settings = get_settings()
        self.api_key = api_key or settings.openai_api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4-turbo-preview"  # Use GPT-4 Turbo for text generation

    def generate_game_analysis(
        self, game_name: str = "VRC High Stakes", num_strategies: int = 8
    ) -> str:
        """
        Generate comprehensive game analysis section.

        Args:
            game_name: Name of the VEX game
            num_strategies: Number of strategies to analyze

        Returns:
            Markdown formatted game analysis
        """
        prompt = f"""
        Create a comprehensive game analysis for VEX Robotics Competition {game_name}.

        Include:
        1. Game Overview (scoring elements, field layout)
        2. Analysis of {num_strategies} different game strategies with pros/cons
        3. Point value breakdown
        4. Optimal strategy recommendation with reasoning
        5. Timeline considerations (autonomous vs driver control)

        Format as a detailed engineering notebook entry with:
        - Clear headings
        - Bullet points for strategies
        - Numerical analysis where relevant
        - Decision matrix comparing strategies

        Write as if you're a high school robotics student documenting your team's analysis.
        Use authentic student voice (enthusiastic but not overly technical).
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
        )

        return response.choices[0].message.content

    def generate_brainstorming_options(
        self, subsystem: str, num_options: int = 3, context: str = ""
    ) -> str:
        """
        Generate brainstorming content showing multiple design options.

        Args:
            subsystem: Subsystem name (e.g., "intake", "drivetrain", "lift")
            num_options: Number of design options to generate
            context: Additional context about requirements

        Returns:
            Markdown formatted brainstorming section
        """
        prompt = f"""
        Create a brainstorming section for a {subsystem} subsystem in VEX Robotics.

        Generate {num_options} distinct design options, each with:
        1. Name/title
        2. Detailed description
        3. Sketch description (what would be drawn)
        4. Pros (3-4 points)
        5. Cons (3-4 points)
        6. Estimated complexity (low/medium/high)
        7. Key components needed

        {f'Context/Requirements: {context}' if context else ''}

        After describing options, include:
        - Decision matrix with weighted criteria (speed, reliability, ease of build, cost, size)
        - Scores for each option (1-5 scale)
        - Final recommendation with clear reasoning

        Write as a high school student documenting the engineering design process.
        Make options genuinely different (not just minor variations).
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,  # Higher temperature for more creative options
            max_tokens=2000,
        )

        return response.choices[0].message.content

    def generate_testing_documentation(
        self,
        subsystem: str,
        test_type: str = "performance",
        num_trials: int = 10,
    ) -> str:
        """
        Generate testing documentation with quantitative data.

        Args:
            subsystem: What was tested
            test_type: Type of test (performance, reliability, speed, etc.)
            num_trials: Number of test trials

        Returns:
            Markdown formatted testing documentation
        """
        prompt = f"""
        Create testing documentation for a VEX robotics {subsystem}.

        Test Type: {test_type}
        Number of Trials: {num_trials}

        Include:
        1. Test Objective (what we're measuring and why)
        2. Test Procedure (step-by-step how test was conducted)
        3. Equipment/Materials used
        4. Data Table with {num_trials} trials showing:
           - Trial number
           - Measured values (appropriate metrics for {test_type})
           - Notes/observations
        5. Data Analysis:
           - Average
           - Best/worst results
           - Consistency analysis
        6. Results & Conclusions
        7. Identified Issues (at least 1-2 problems found)
        8. Next Steps / Improvements planned

        Make the data realistic for a VEX robotics test.
        Include both successes AND failures.
        Write as a student documenting their testing process.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )

        return response.choices[0].message.content

    def generate_design_iteration(
        self,
        subsystem: str,
        iteration_number: int,
        previous_issues: str = "",
    ) -> str:
        """
        Generate design iteration documentation.

        Args:
            subsystem: What subsystem is being iterated
            iteration_number: Which iteration (1, 2, 3, etc.)
            previous_issues: Issues from previous iteration to address

        Returns:
            Markdown formatted design iteration entry
        """
        prompt = f"""
        Create design iteration documentation for {subsystem} - Design Cycle {iteration_number}.

        {f'Previous Issues to Address: {previous_issues}' if previous_issues else 'This is the first iteration.'}

        Include:
        1. Iteration Goal (what we're trying to improve)
        2. Changes Made (specific modifications from previous version)
        3. Reasoning (why these changes address the issues)
        4. Build Documentation:
           - Components changed
           - Construction steps
           - Technical details (gear ratios, measurements, etc.)
        5. Expected Improvements
        6. Test Results (brief summary)
        7. What We Learned
        8. Next Steps

        Write as a student documenting their iterative design process.
        Show clear improvement from previous version.
        {f'Make sure the changes directly address: {previous_issues}' if previous_issues else ''}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )

        return response.choices[0].message.content

    def generate_meeting_notes(
        self,
        meeting_number: int,
        focus_areas: List[str] = None,
        team_size: int = 4,
    ) -> str:
        """
        Generate team meeting notes.

        Args:
            meeting_number: Meeting number
            focus_areas: What was discussed (e.g., ["drivetrain", "autonomous"])
            team_size: Number of team members

        Returns:
            Markdown formatted meeting notes
        """
        focus_areas = focus_areas or ["general progress"]

        prompt = f"""
        Create team meeting notes for Meeting #{meeting_number} of a VEX robotics team.

        Team Size: {team_size} students
        Focus Areas: {', '.join(focus_areas)}

        Include:
        1. Meeting Header:
           - Date (use realistic date in current season)
           - Time & Duration
           - Attendees (generate {team_size} realistic names with roles)
        2. Agenda items related to: {', '.join(focus_areas)}
        3. Discussion points for each agenda item
        4. Decisions Made (at least 2-3 concrete decisions)
        5. Action Items:
           - Task description
           - Assigned to (team member name)
           - Due date
        6. Goals for Next Meeting
        7. Notes/Observations

        Write as authentic high school student meeting minutes.
        Include some informal language but keep it organized.
        Show collaborative decision-making process.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200,
        )

        return response.choices[0].message.content

    def generate_build_documentation(
        self,
        component: str,
        detail_level: str = "high",
    ) -> str:
        """
        Generate detailed build documentation.

        Args:
            component: What was built
            detail_level: "high" for very detailed, "medium" for moderate

        Returns:
            Markdown formatted build documentation
        """
        prompt = f"""
        Create detailed build documentation for a {component} in VEX Robotics.

        Detail Level: {detail_level}

        Include:
        1. Component Overview (purpose and design goals)
        2. Parts List:
           - VEX part numbers
           - Quantities
           - Special components
        3. Build Instructions:
           - Step-by-step assembly
           - {"Highly detailed with measurements and specifics" if detail_level == "high" else "Clear but moderate detail"}
           - Critical points to watch
        4. Technical Specifications:
           - Dimensions
           - Gear ratios (if applicable)
           - Weight
        5. CAD/Diagram Description (describe what drawings would show)
        6. Build Challenges & Solutions
        7. Verification/Testing (how to ensure it's built correctly)

        Make it detailed enough that someone could recreate this component.
        Write as a student documenting their build process.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1800,
        )

        return response.choices[0].message.content

    def generate_programming_documentation(
        self,
        feature: str,
        language: str = "C++",
    ) -> str:
        """
        Generate programming documentation.

        Args:
            feature: What feature/function was programmed
            language: Programming language used

        Returns:
            Markdown formatted programming documentation
        """
        prompt = f"""
        Create programming documentation for a {feature} feature in VEX Robotics.

        Language: {language}

        Include:
        1. Feature Description (what it does and why)
        2. Algorithm/Logic Explanation
        3. Pseudocode or flowchart description
        4. Code snippet (key parts, not entire program)
        5. Variables/Constants used
        6. Testing approach
        7. Challenges encountered
        8. Improvements made
        9. Future enhancements planned

        Write as a student explaining their code.
        Include comments in code.
        Explain technical concepts clearly.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )

        return response.choices[0].message.content

    def generate_decision_matrix(
        self,
        options: List[str],
        criteria: List[str] = None,
    ) -> str:
        """
        Generate a decision matrix comparing options.

        Args:
            options: List of options to compare
            criteria: Criteria to evaluate (if None, uses defaults)

        Returns:
            Markdown formatted decision matrix
        """
        criteria = criteria or [
            "Speed/Performance",
            "Reliability",
            "Ease of Build",
            "Cost",
            "Size/Weight"
        ]

        prompt = f"""
        Create a decision matrix comparing these options: {', '.join(options)}

        Criteria (rate 1-5 for each):
        {chr(10).join(f'- {c}' for c in criteria)}

        Include:
        1. Criteria weights (importance 1-10 for each criterion)
        2. Scores table:
           - Each option rated on each criterion (1-5)
           - Raw scores
           - Weighted scores
        3. Total weighted scores
        4. Clear winner with explanation
        5. Runner-up discussion

        Present as a proper decision matrix with calculations.
        Explain why scores were assigned.
        Make the winner clear but close enough to show real consideration.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200,
        )

        return response.choices[0].message.content

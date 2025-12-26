"""Specialized generator for brainstorming sections."""

from typing import List, Dict
from .content_generator import ContentGenerator


class BrainstormGenerator(ContentGenerator):
    """Generate comprehensive brainstorming sections with multiple options."""

    COMMON_SUBSYSTEMS = [
        "intake",
        "drivetrain",
        "lift",
        "scoring_mechanism",
        "mobile_goal_mechanism",
        "ring_manipulator",
        "autonomous_selector",
        "expansion_mechanism",
    ]

    def generate_complete_brainstorm_section(
        self,
        subsystem: str,
        game_context: str = "VRC High Stakes",
    ) -> Dict[str, str]:
        """
        Generate a complete brainstorming section with all components.

        Args:
            subsystem: Subsystem to brainstorm
            game_context: Game context for relevance

        Returns:
            Dict with keys: initial_analysis, options, decision_matrix, conclusion
        """
        # Initial analysis
        analysis_prompt = f"""
        Write an initial analysis section for brainstorming a {subsystem} for {game_context}.

        Include:
        - Purpose of this subsystem
        - Key requirements based on game rules
        - Constraints to consider (size, weight, rules)
        - Success criteria (what makes a good {subsystem})

        Write as a student starting the design process.
        2-3 paragraphs, conversational but thorough.
        """

        initial_analysis = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.7,
            max_tokens=600,
        ).choices[0].message.content

        # Generate 3+ options
        options = self.generate_brainstorming_options(
            subsystem=subsystem,
            num_options=4,
            context=game_context,
        )

        # Decision matrix
        decision_matrix = self.generate_decision_matrix(
            options=[f"Option A", f"Option B", f"Option C", f"Option D"],
            criteria=["Speed", "Reliability", "Build Complexity", "Cost", "Effectiveness"],
        )

        # Conclusion
        conclusion_prompt = f"""
        Write a conclusion for selecting a {subsystem} design.

        Briefly state:
        - Which option was chosen
        - Why it was the best choice
        - What the team will do next (move to CAD, prototyping, etc.)

        1 paragraph, enthusiastic student voice.
        """

        conclusion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": conclusion_prompt}],
            temperature=0.7,
            max_tokens=300,
        ).choices[0].message.content

        return {
            "initial_analysis": initial_analysis,
            "options": options,
            "decision_matrix": decision_matrix,
            "conclusion": conclusion,
        }

    def generate_full_robot_brainstorm(
        self,
        subsystems: List[str] = None,
    ) -> Dict[str, Dict]:
        """
        Generate brainstorming for all major robot subsystems.

        Args:
            subsystems: List of subsystems (if None, uses common ones)

        Returns:
            Dict mapping subsystem name to brainstorm sections
        """
        subsystems = subsystems or ["drivetrain", "intake", "scoring_mechanism"]

        results = {}
        for subsystem in subsystems:
            results[subsystem] = self.generate_complete_brainstorm_section(subsystem)

        return results

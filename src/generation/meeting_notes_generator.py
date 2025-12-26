"""Generate realistic team meeting notes."""

import random
from datetime import datetime, timedelta
from typing import List, Optional
from .content_generator import ContentGenerator


class MeetingNotesGenerator(ContentGenerator):
    """Generate team meeting notes."""

    TEAM_ROLES = [
        "Team Captain",
        "Lead Builder",
        "Lead Programmer",
        "CAD Specialist",
        "Scout/Strategy",
        "Notebook Lead",
        "Driver",
    ]

    STUDENT_NAMES = [
        "Alex Chen",
        "Jordan Smith",
        "Sam Patel",
        "Morgan Davis",
        "Riley Johnson",
        "Casey Williams",
        "Taylor Brown",
        "Drew Martinez",
    ]

    def generate_season_meetings(
        self,
        num_meetings: int = 15,
        team_size: int = 5,
    ) -> List[str]:
        """
        Generate a full season's worth of meeting notes.

        Args:
            num_meetings: Number of meetings to generate
            team_size: Team size

        Returns:
            List of meeting note documents
        """
        meetings = []
        team_members = random.sample(self.STUDENT_NAMES, team_size)
        roles = self.TEAM_ROLES[:team_size]

        # Assign roles to members
        team_roster = {name: role for name, role in zip(team_members, roles)}

        # Generate meetings with progression
        base_date = datetime(2024, 9, 1)  # Start of season

        phases = [
            ("kickoff", ["game_analysis", "strategy_planning"], 2),
            ("design", ["brainstorming", "CAD", "parts_ordering"], 4),
            ("build", ["building", "testing", "programming"], 5),
            ("competition_prep", ["driver_practice", "autonomous", "documentation"], 3),
            ("post_competition", ["improvements", "next_event"], 1),
        ]

        meeting_num = 1
        for phase_name, topics, num_phase_meetings in phases:
            for i in range(num_phase_meetings):
                if meeting_num > num_meetings:
                    break

                # Calculate meeting date (roughly 1 week apart)
                meeting_date = base_date + timedelta(weeks=meeting_num - 1)

                # Pick 2-3 topics for this meeting
                meeting_topics = random.sample(topics, min(len(topics), random.randint(2, 3)))

                meeting_doc = self._generate_single_meeting(
                    meeting_num=meeting_num,
                    date=meeting_date,
                    team_roster=team_roster,
                    topics=meeting_topics,
                    phase=phase_name,
                )

                meetings.append(meeting_doc)
                meeting_num += 1

        return meetings

    def _generate_single_meeting(
        self,
        meeting_num: int,
        date: datetime,
        team_roster: dict,
        topics: List[str],
        phase: str,
    ) -> str:
        """Generate a single meeting notes document."""

        # Determine attendees (sometimes not everyone)
        all_members = list(team_roster.keys())
        num_attending = random.randint(max(3, len(all_members) - 2), len(all_members))
        attendees = random.sample(all_members, num_attending)

        # Generate duration
        duration = random.randint(60, 150)  # minutes

        doc = f"""# Team Meeting #{meeting_num}

**Date**: {date.strftime('%Y-%m-%d')}
**Time**: 3:30 PM - {self._add_minutes_to_time('3:30 PM', duration)}
**Duration**: {duration} minutes
**Phase**: {phase.replace('_', ' ').title()}

## Attendees
"""

        for name in attendees:
            role = team_roster[name]
            doc += f"- {name} ({role})\n"

        if len(attendees) < len(all_members):
            absent = set(all_members) - set(attendees)
            doc += f"\n**Absent**: {', '.join(absent)}\n"

        doc += f"""
## Agenda
{chr(10).join(f'{i + 1}. {topic.replace("_", " ").title()}' for i, topic in enumerate(topics))}

## Discussion

"""

        # Generate discussion for each topic
        for topic in topics:
            doc += self._generate_topic_discussion(topic, attendees, team_roster)

        # Generate decisions
        num_decisions = random.randint(2, 4)
        doc += "\n## Decisions Made\n\n"

        decisions = self._generate_decisions(topics, phase, num_decisions)
        for i, decision in enumerate(decisions, 1):
            doc += f"{i}. {decision}\n"

        # Generate action items
        num_actions = random.randint(3, 6)
        doc += "\n## Action Items\n\n"
        doc += "| Task | Assigned To | Due Date |\n"
        doc += "|------|-------------|----------|\n"

        actions = self._generate_action_items(topics, attendees, date, num_actions)
        for action in actions:
            doc += f"| {action['task']} | {action['assigned']} | {action['due']} |\n"

        # Goals for next meeting
        doc += f"\n## Goals for Next Meeting\n\n"
        next_goals = self._generate_next_goals(phase, topics)
        for goal in next_goals:
            doc += f"- {goal}\n"

        doc += f"\n**Minutes recorded by**: {random.choice(attendees)}\n"

        return doc

    def _generate_topic_discussion(
        self, topic: str, attendees: List[str], roster: dict
    ) -> str:
        """Generate discussion content for a topic."""

        discussions = {
            "game_analysis": f"""### Game Analysis
{random.choice(attendees)} presented initial game analysis. Team discussed scoring strategies and identified key game elements. Focused on point values and optimal autonomous routines.
""",
            "strategy_planning": f"""### Strategy Planning
Team evaluated 4 different game strategies. Used decision matrix to compare. Decided on balanced approach focusing on consistency over high risk/reward.
""",
            "brainstorming": f"""### Brainstorming Session
Brainstormed designs for intake mechanism. Generated 4 distinct options ranging from simple to complex. Will create decision matrix next meeting.
""",
            "CAD": f"""### CAD Progress
{[name for name, role in roster.items() if 'CAD' in role or 'Builder' in role][0] if any('CAD' in role or 'Builder' in role for role in roster.values()) else random.choice(attendees)} showed current CAD model. Identified interference issues with lift mechanism. Will revise and re-test clearances.
""",
            "building": f"""### Build Progress
Team completed drivetrain assembly. Started on intake system. Ran into issue with motor mounting - solved by using standoffs. Build is ~60% complete.
""",
            "testing": f"""### Testing Update
Ran performance tests on intake. Results below target (15 rings/min vs 20 target). Identified friction issue. Planning design iteration to address.
""",
            "programming": f"""### Programming Status
{[name for name, role in roster.items() if 'Programmer' in role][0] if any('Programmer' in role for role in roster.values()) else random.choice(attendees)} demonstrated autonomous routine. 80% reliable. Need to tune PID values and add sensor feedback.
""",
            "driver_practice": f"""### Driver Practice
Driver ran practice matches. Averaging 150 points in driver control. Need more practice with autonomous selector. Scheduled extra practice sessions.
""",
            "improvements": f"""### Post-Competition Improvements
Reviewed match videos and identified 3 key areas for improvement. Created priority list for next competition. Will implement highest priority changes first.
""",
        }

        return discussions.get(topic, f"### {topic.replace('_', ' ').title()}\nTeam discussed {topic} and made progress.\n\n")

    def _generate_decisions(self, topics: List[str], phase: str, num: int) -> List[str]:
        """Generate realistic decisions."""

        decision_pool = [
            "Selected Option B for intake design due to highest decision matrix score",
            "Agreed to prioritize reliability over speed in current build phase",
            "Approved budget request for additional motors ($80)",
            "Changed autonomous strategy to focus on consistency",
            "Decided to implement flywheel with 5:3 gear ratio",
            "Split team into two sub-teams: build and programming",
            "Set goal of 180 points per match for next competition",
            "Will use blue lexan for custom parts",
            "Approved final robot dimensions: 18x18x18 inches",
        ]

        return random.sample(decision_pool, min(num, len(decision_pool)))

    def _generate_action_items(
        self, topics: List[str], attendees: List[str], base_date: datetime, num: int
    ) -> List[dict]:
        """Generate action items."""

        task_pool = [
            "Finalize CAD for intake system",
            "Order parts from VEX website",
            "Complete autonomous programming",
            "Update engineering notebook with testing data",
            "Build prototype of scoring mechanism",
            "Tune PID controllers for drivetrain",
            "Create decision matrix for lift design",
            "Film and analyze driver practice",
            "Research other teams' designs on VEX Forum",
            "Test battery life under full load",
        ]

        actions = []
        selected_tasks = random.sample(task_pool, min(num, len(task_pool)))

        for i, task in enumerate(selected_tasks):
            due_date = base_date + timedelta(days=random.randint(3, 10))
            actions.append({
                "task": task,
                "assigned": random.choice(attendees),
                "due": due_date.strftime("%Y-%m-%d"),
            })

        return actions

    def _generate_next_goals(self, phase: str, topics: List[str]) -> List[str]:
        """Generate goals for next meeting."""

        goals = {
            "kickoff": [
                "Complete full game analysis with 8 strategies",
                "Finalize robot strategy and design approach",
            ],
            "design": [
                "Present CAD models for all subsystems",
                "Finalize parts order",
                "Begin prototype build",
            ],
            "build": [
                "Complete robot assembly",
                "Begin driver practice",
                "Run full system tests",
            ],
            "competition_prep": [
                "Finalize autonomous routines",
                "Complete pre-competition checklist",
                "Practice driver skills",
            ],
        }

        return goals.get(phase, ["Continue progress on current tasks"])

    def _add_minutes_to_time(self, time_str: str, minutes: int) -> str:
        """Add minutes to a time string."""
        # Simple implementation for PM times
        hour, minute = map(int, time_str.replace(' PM', '').split(':'))
        total_minutes = hour * 60 + minute + minutes
        new_hour = (total_minutes // 60) % 12
        if new_hour == 0:
            new_hour = 12
        new_minute = total_minutes % 60
        return f"{new_hour}:{new_minute:02d} PM"

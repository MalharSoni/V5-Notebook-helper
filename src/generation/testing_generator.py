"""Generate realistic testing data and documentation."""

import random
from typing import List, Dict, Optional
from .content_generator import ContentGenerator


class TestingDataGenerator(ContentGenerator):
    """Generate realistic testing documentation with data."""

    def generate_realistic_test_data(
        self,
        test_type: str,
        num_trials: int = 10,
        mean: float = 100,
        std_dev: float = 10,
        unit: str = "units",
    ) -> List[Dict]:
        """
        Generate realistic test data with variation.

        Args:
            test_type: Type of test
            num_trials: Number of trials
            mean: Mean value
            std_dev: Standard deviation
            unit: Unit of measurement

        Returns:
            List of trial dictionaries
        """
        trials = []

        for i in range(1, num_trials + 1):
            # Generate realistic data with some variation
            value = random.gauss(mean, std_dev)
            value = max(0, value)  # No negative values

            # Add occasional outliers
            if random.random() < 0.1:  # 10% chance
                value = value * random.choice([0.5, 1.5])

            trials.append({
                "trial": i,
                "value": round(value, 2),
                "unit": unit,
                "notes": self._generate_trial_note(i, value, mean),
            })

        return trials

    def _generate_trial_note(self, trial_num: int, value: float, mean: float) -> str:
        """Generate realistic trial notes."""
        if abs(value - mean) > mean * 0.3:
            notes = [
                "Outlier - investigating cause",
                "Mechanical slip detected",
                "Battery voltage low",
                "Unusual result - retesting",
                "Driver error - ball missed intake",
            ]
            return random.choice(notes)
        elif trial_num == 1:
            return "First trial - baseline"
        elif trial_num % 3 == 0:
            return "Consistent with previous trials"
        else:
            return ""

    def generate_performance_test(
        self,
        subsystem: str,
        metric: str,
        target_value: float,
    ) -> str:
        """
        Generate complete performance test documentation.

        Args:
            subsystem: What was tested
            metric: What was measured (e.g., "rings per minute", "cycle time")
            target_value: Target performance

        Returns:
            Markdown formatted test documentation with realistic data
        """
        # Generate realistic data
        trials = self.generate_realistic_test_data(
            test_type="performance",
            num_trials=10,
            mean=target_value * 0.85,  # Average slightly below target
            std_dev=target_value * 0.15,
            unit=metric.split()[-1] if " " in metric else "units",
        )

        # Calculate statistics
        values = [t["value"] for t in trials]
        avg = sum(values) / len(values)
        best = max(values)
        worst = min(values)
        success_rate = len([v for v in values if v >= target_value * 0.8]) / len(values)

        # Build documentation
        doc = f"""# {subsystem.title()} Performance Test

## Test Objective
Measure {metric} to evaluate {subsystem} performance and determine if we meet our target of {target_value}.

## Test Procedure
1. Set up robot on practice field
2. Run {subsystem} for full cycle
3. Measure {metric}
4. Record results
5. Repeat for 10 trials

## Equipment
- Competition robot
- Stopwatch/timer
- Field elements
- Fully charged battery (12.5V)

## Test Data

| Trial | {metric.title()} | Notes |
|-------|---------|-------|
"""

        for trial in trials:
            doc += f"| {trial['trial']} | {trial['value']} | {trial['notes']} |\n"

        doc += f"""
## Data Analysis

- **Average**: {avg:.2f}
- **Best**: {best:.2f}
- **Worst**: {worst:.2f}
- **Target**: {target_value}
- **Success Rate**: {success_rate * 100:.1f}% (trials within 80% of target)

## Results & Conclusions

{"✓ MEETS TARGET: " if avg >= target_value * 0.9 else "✗ BELOW TARGET: "}
Average performance of {avg:.2f} {"meets" if avg >= target_value * 0.9 else "does not meet"} our target of {target_value}.

### Observations:
- Performance is {"consistent" if max(values) - min(values) < avg * 0.4 else "inconsistent"}
- {"Several outliers detected - need to investigate" if len([v for v in values if abs(v - avg) > avg * 0.3]) > 2 else "Data shows good consistency"}

## Identified Issues
1. {f"Performance below target by {((target_value - avg) / target_value * 100):.1f}%" if avg < target_value else "Occasional performance drops need investigation"}
2. Need to improve consistency between trials

## Next Steps
1. {"Increase motor speed / gear ratio" if avg < target_value else "Optimize for consistency"}
2. Test with fresh battery to isolate power issues
3. Film trials to identify failure modes
4. Run iteration 2 with improvements

**Date**: {self._get_realistic_date()}
**Tested by**: Team members present
"""

        return doc

    def _get_realistic_date(self) -> str:
        """Generate realistic date in current season."""
        import datetime
        # Random date in current academic year
        month = random.randint(9, 12) if random.random() < 0.6 else random.randint(1, 3)
        day = random.randint(1, 28)
        year = 2024 if month >= 9 else 2025
        return f"{year}-{month:02d}-{day:02d}"

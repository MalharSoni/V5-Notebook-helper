# VRC Engineering Notebook Structure Guide

> **Purpose**: Complete guide to structuring a winning VRC engineering notebook. Covers all required sections, content guidelines, and organizational best practices.

---

## Table of Contents
1. [Front Matter (Introductory Pages)](#front-matter)
2. [Game Analysis Section](#game-analysis-section)
3. [Design Process Sections](#design-process-sections)
4. [Programming Documentation](#programming-documentation)
5. [Testing & Evaluation](#testing--evaluation)
6. [Tournament Analysis](#tournament-analysis)
7. [Project Management](#project-management)
8. [Appendices](#appendices)
9. [Formatting Standards](#formatting-standards)

---

## Front Matter

### 1. Title/Cover Page
**Required Elements:**
- Team number prominently displayed
- Team name
- Team logo
- Season identifier (e.g., "2024-2025 High Stakes")
- Start and end dates

**Best Practices:**
- Create memorable first impression for judges
- Use consistent branding colors
- Professional, clean design

### 2. Table of Contents
**Required Elements:**
- All major sections listed
- Page numbers for each section
- Sub-sections clearly organized

**Best Practices:**
- **Color-code entries by Engineering Design Process stage**
- Use consistent formatting
- Update as notebook grows
- Include hyperlinks if digital

**Recommended Color Coding:**
| Color | Section Type |
|-------|-------------|
| Yellow | Introduction/Team |
| Blue | Mechanical Design |
| Green | Programming |
| Purple | Strategy |
| Orange | Testing |
| Red | Competition/Admin |

### 3. Engineering Design Process Overview
**Required Elements:**
- Graphic or text describing the cyclical EDP
- Explanation of how team uses the process
- **Cite sources for any borrowed imagery**

**EDP Steps to Document:**
1. Identify the Problem/Challenge
2. Brainstorm Solutions
3. Select Best Solution (Decision Matrix)
4. Build/Prototype
5. Test and Evaluate
6. Iterate and Improve

### 4. Team Profile/Introduction
**Required Elements:**
- Brief team description
- Member photos with names
- Member roles and responsibilities
- Member experience/background

**Best Practices:**
- Include grade levels
- Mention areas of expertise
- Show team personality
- Helps judges connect faces to teams

### 5. Notebook Formatting Guide
**Required Elements:**
- Explanation of organizational system
- Version history tracking method
- How pages are dated
- How contributors are identified

**Best Practices:**
- Include legend for color coding
- Explain margin tabs/section identifiers
- Document revision process

### 6. Season Goals
**Required Elements:**
- 2-4 team objectives for the season
- Measurable where possible

**Example Goals:**
- Qualify for State Championship
- Win Design Award at 2+ tournaments
- Achieve 150+ Programming Skills score
- Complete 3 full design iterations

### 7. GANTT Chart / Timeline
**Required Elements:**
- Visual timeline allocating time to each project phase
- Major milestones identified
- Competition dates marked

**Best Practices:**
- Shows advanced project management
- Update throughout season
- Track actual vs. planned progress

### 8. Budget
**Required Elements:**
- Financial resource planning
- Cost breakdown by category
- Total budget

**Recommended Categories:**
- Mechanical Parts
- Field Elements
- Competition Registration
- Travel
- Marketing/Outreach
- Miscellaneous

---

## Game Analysis Section

> **Rubric Requirement**: "Identify the game and robot design challenges in detail at the start of each design process cycle with words and pictures."

### 1. Game Goals
**Required Content:**
- Explicit statement of scoring objectives
- Point values for each scoring action
- Winning conditions

**For High Stakes 2024-2025:**
- Rings on Stakes: 1 point each
- Top Ring on Stake: 3 points
- Positive Corner doubles values
- Negative Corner zeros values
- Autonomous Bonus: 6 points
- Climbing points

### 2. Field Specifications
**Required Content:**
- Field dimensions (12' x 12' for VRC)
- All field element dimensions
- Game piece specifications
- Starting positions

**Best Practices:**
- Include field diagrams with measurements
- Document stake locations and heights
- Note zone boundaries

### 3. Rules Discussion
**Required Content:**
- Key game rules summarized **in your own words**
- Do NOT copy game manual verbatim
- Penalty rules and conditions
- Match structure (15s auton + 1:45 driver)

**Important Rules to Cover:**
- Scoring definitions
- Robot restrictions
- Game-specific rules
- Autonomous Win Point conditions

### 4. Strategy Analysis
**Required Content:**
- List 7-8 potential viable strategies
- Advantages/disadvantages for each
- Strategy selection reasoning

**Strategy Categories to Analyze:**
- Offensive strategies
- Defensive strategies
- Autonomous strategies
- End-game strategies
- Alliance strategies

---

## Design Process Sections

### Design Constraints
**Required Content:**
- VEX legal materials and parts
- Size limitations (18" cube starting)
- Expansion rules (22" in one direction)
- Motor limitations (88W total)
- Pneumatic limitations (100 PSI max)

### Brainstorming (Per Subsystem)
> **Rubric Requirement**: "List three or more possible solutions to the challenge with labeled diagrams."

**Required for Each Subsystem:**
- Minimum 3 unique designs
- Full CAD drawings OR detailed sketches
- Every component labeled
- Pros and cons for each design
- Citations for external inspiration

**Subsystems to Document:**
- Drivetrain
- Intake System
- Scoring Mechanism
- Climbing Mechanism
- Expansion Mechanism
- Any game-specific mechanisms

### Decision Matrix
> **Rubric Requirement**: "Explain why the solution was selected through testing and/or a decision matrix."

**Required Elements:**
- Criteria list with weights
- Score each design against criteria
- Mathematical calculation
- Winner identification with justification

**Sample Criteria:**
| Criterion | Weight |
|-----------|--------|
| Speed | 20% |
| Reliability | 25% |
| Ease of Build | 15% |
| Versatility | 20% |
| Weight | 10% |
| Cost | 10% |

### CAD Plans
**Required Content:**
- Detailed 3D renderings
- Multiple angles/views
- Measurements labeled
- Bill of materials

**Best Practices:**
- Use Fusion 360, Inventor, or similar
- Include isometric and orthographic views
- Show assembly order
- Document CAD file versions

### Build Documentation
> **Rubric Requirement**: "Record the steps to build and program the solution. Include enough detail that the reader can follow the logic used and recreate the robot design."

**Required Content:**
- Step-by-step build instructions
- Photos of build progress
- Component identification
- Assembly order
- Tools and materials used

**Best Practices:**
- Heavily label all images
- Explain purpose of every component
- Document any modifications from CAD
- Include build time estimates

---

## Programming Documentation

### Code Organization
**Required Content:**
- Overall code structure explanation
- File organization
- Libraries used (with citations)

### Driver Control
**Document:**
- Control scheme
- Button mappings
- Speed curves/adjustments
- Macros and shortcuts

### Autonomous Routines
**Document:**
- Route planning and logic
- Sensor usage
- Timing and sequencing
- Multiple autonomous options

### Odometry/Positioning
**Document:**
- Tracking wheel setup
- Calibration process
- Error correction methods
- Coordinate system used

### Code Changelog
**Required Format:**
```
Date: [DATE]
Author: [NAME]
Changes:
- [Change 1]
- [Change 2]
Reason: [Why changes were made]
```

### Code Snippets
**Best Practices:**
- Include actual code with explanations
- Highlight key algorithms
- Explain logic behind decisions
- Document debugging process

---

## Testing & Evaluation

> **Rubric Requirement**: "Record all the steps to test the solution, including test results."

### Test Planning
**Required Elements:**
- Clear, measurable metrics
- Test procedures documented
- Expected outcomes stated
- Variables identified

### Test Documentation Format
```
Test Name: [NAME]
Date: [DATE]
Objective: [What you're testing]
Procedure:
1. [Step 1]
2. [Step 2]
...
Results:
| Trial | Result | Pass/Fail |
|-------|--------|-----------|
| 1     | X      | Pass      |
| 2     | Y      | Fail      |
...
Conclusion: [What was learned]
Next Steps: [What to do with results]
```

### Types of Tests
- **Reliability Tests**: Success rate over multiple trials
- **Speed Tests**: Time to complete actions
- **Accuracy Tests**: Precision of movements
- **Stress Tests**: Performance under extreme conditions
- **Integration Tests**: Multiple systems working together

### Evaluation Against Requirements
**Required:**
- Compare results to initial requirements
- Document which requirements are met
- Identify areas for improvement
- Drive next design iteration

---

## Tournament Analysis

### Pre-Competition Preparation
- Match schedule review
- Alliance selection strategy
- Scouting plan

### Match Documentation
**For Each Match:**
- Match number and alliance
- Score breakdown
- What worked well
- What didn't work
- Specific malfunctions and root causes

### Post-Competition Analysis
**Required:**
- Overall performance summary
- Ranking and results
- Competing team strategy analysis
- Lessons learned
- Improvements for next iteration

---

## Project Management

> **Rubric Requirement**: "Provides a complete record of team and project assignments; team meeting notes including goals, decisions, and accomplishments."

### Meeting Minutes Format
```
Date: [DATE]
Attendees: [LIST]
Duration: [TIME]

Goals for Today:
1. [Goal 1]
2. [Goal 2]

Discussion:
- [Topic 1]
- [Topic 2]

Decisions Made:
- [Decision 1]
- [Decision 2]

Accomplishments:
- [What was completed]

Action Items:
| Task | Assignee | Due Date | Status |
|------|----------|----------|--------|
| X    | Name     | Date     | Status |

Goals for Next Meeting:
1. [Goal 1]
2. [Goal 2]
```

### Team Roles
**Document Specific Roles:**
- Builder(s)
- Designer(s)
- Programmer(s)
- Driver(s)
- Notebook Manager
- Project Manager
- Scouting Lead
- Any custom roles

### Resource Tracking
**Document:**
- Time spent on tasks
- Parts inventory
- Budget expenditures
- Schedule adherence

---

## Appendices

> **Note**: Judges do NOT consider appendix content for rubric scores. Use for reference materials only.

### Acceptable Appendix Content:
- External research documents
- Reference images from other sources
- Full code printouts
- Raw data from tests
- Competition brackets/results
- Award certificates
- Sponsor information

### Organization:
- Clearly labeled appendix sections
- Table of contents for appendices
- Referenced in main notebook where relevant

---

## Formatting Standards

### Page Layout
**Required Elements:**
- Header: Project name, page title, page number
- Footer: Designer name, Witness name, Date
- Margin tabs for section identification
- Consistent grid/line backgrounds

### Typography
- Consistent fonts throughout
- Clear hierarchy (headings, subheadings, body)
- Readable font sizes (minimum 10pt)
- Professional appearance

### Images
- High quality, well-lit photos
- All images labeled
- Captions explaining relevance
- Consistent sizing and placement

### Color Usage
- Consistent color scheme throughout
- Colors aid organization, not distract
- High contrast for readability
- Color-blind friendly when possible

### Dating and Attribution
**Every Page Must Have:**
- Date of creation/edit
- Name of content creator
- Witness signature (if physical)

---

## Quick Section Checklist

### Front Matter
- [ ] Cover page with team info
- [ ] Table of contents (color-coded)
- [ ] EDP overview
- [ ] Team introduction with photos
- [ ] Formatting guide
- [ ] Season goals
- [ ] GANTT chart
- [ ] Budget

### Game Analysis
- [ ] Game goals and scoring
- [ ] Field specifications with diagrams
- [ ] Rules summary (own words)
- [ ] 7-8 strategies analyzed

### Design Process (Per Iteration)
- [ ] Design constraints
- [ ] 3+ brainstorm ideas with diagrams
- [ ] Decision matrix
- [ ] CAD plans
- [ ] Build documentation

### Programming
- [ ] Code structure
- [ ] Driver control documentation
- [ ] Autonomous routines
- [ ] Code changelog

### Testing
- [ ] Test procedures
- [ ] Results with data
- [ ] Evaluation against requirements
- [ ] Conclusions and next steps

### Competitions
- [ ] Match analysis
- [ ] Strategy observations
- [ ] Lessons learned

### Project Management
- [ ] Meeting minutes
- [ ] Team roles
- [ ] Resource tracking

---

*Document compiled for Team 839Z - Caution Tape ZOOM!*
*Last updated: December 2025*

"""Vision analysis using GPT-4 Vision to analyze notebook pages."""

import base64
from pathlib import Path
from typing import List, Optional

from openai import OpenAI
from PIL import Image

from ..config import get_settings
from ..models import NotebookPage, PageAnalysis


class VisionAnalyzer:
    """Analyzes notebook pages using GPT-4 Vision API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the vision analyzer.

        Args:
            api_key: OpenAI API key. If None, uses config settings.
        """
        settings = get_settings()
        self.api_key = api_key or settings.openai_api_key
        self.model = settings.openai_model
        self.client = OpenAI(api_key=self.api_key)

    def encode_image(self, image_path: Path) -> str:
        """
        Encode image to base64 for API.

        Args:
            image_path: Path to image file

        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def analyze_page(self, page: NotebookPage) -> PageAnalysis:
        """
        Analyze a single notebook page using GPT-4 Vision.

        Args:
            page: NotebookPage to analyze

        Returns:
            PageAnalysis with findings
        """
        # Encode image
        base64_image = self.encode_image(page.file_path)

        # Create prompt for analysis
        prompt = """
        Analyze this VEX robotics engineering notebook page.

        Identify:
        1. Content Type (cover, table_of_contents, game_analysis, design, brainstorming,
           testing, meeting_notes, build_documentation, programming, competition, appendix, other)
        2. Brief Summary (2-3 sentences)
        3. Relevant Rubric Categories (EN1-EN10):
           - EN1: Identify the Challenge
           - EN2: Student-Centered Policy
           - EN3: Academic Honesty
           - EN4: Brainstorm Solutions (3+ options with diagrams)
           - EN5: Build and Program Documentation
           - EN6: Test and Record Results
           - EN7: Design Iterations
           - EN8: Project Management
           - EN9: Sequential Documentation (dates/timestamps)
           - EN10: Appendices
        4. Key Elements Found:
           - brainstorming: true/false (3+ design options shown)
           - decision_matrix: true/false
           - cad_drawings: true/false
           - testing_data: true/false (quantitative data present)
           - meeting_notes: true/false
           - dates_timestamps: true/false
           - design_iteration: true/false (shows progression)
           - failure_documentation: true/false
        5. Notes (any important observations)

        Respond in this exact format:
        CONTENT_TYPE: [type]
        SUMMARY: [summary]
        RUBRIC_CATEGORIES: [comma-separated EN codes]
        KEY_ELEMENTS: [JSON object with true/false for each element]
        NOTES: [observations]
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1000,
            )

            # Parse response
            content = response.choices[0].message.content
            return self._parse_analysis_response(page.page_number, content)

        except Exception as e:
            # Return basic analysis on error
            return PageAnalysis(
                page_number=page.page_number,
                content_type="error",
                summary=f"Error analyzing page: {str(e)}",
                rubric_categories=[],
                key_elements={},
                notes=f"Analysis failed: {str(e)}",
            )

    def _parse_analysis_response(
        self, page_number: int, response: str
    ) -> PageAnalysis:
        """
        Parse the GPT-4 Vision response into PageAnalysis.

        Args:
            page_number: Page number being analyzed
            response: Raw response text from API

        Returns:
            Parsed PageAnalysis object
        """
        import json

        lines = response.strip().split("\n")
        data = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key == "CONTENT_TYPE":
                    data["content_type"] = value
                elif key == "SUMMARY":
                    data["summary"] = value
                elif key == "RUBRIC_CATEGORIES":
                    data["rubric_categories"] = [
                        cat.strip() for cat in value.split(",") if cat.strip()
                    ]
                elif key == "KEY_ELEMENTS":
                    try:
                        data["key_elements"] = json.loads(value)
                    except json.JSONDecodeError:
                        data["key_elements"] = {}
                elif key == "NOTES":
                    data["notes"] = value

        return PageAnalysis(
            page_number=page_number,
            content_type=data.get("content_type", "unknown"),
            summary=data.get("summary", "No summary available"),
            rubric_categories=data.get("rubric_categories", []),
            key_elements=data.get("key_elements", {}),
            notes=data.get("notes", ""),
        )

    def analyze_pages(
        self, pages: List[NotebookPage], batch_size: int = 10
    ) -> List[PageAnalysis]:
        """
        Analyze multiple pages.

        Args:
            pages: List of NotebookPages to analyze
            batch_size: Number of pages to analyze in each batch

        Returns:
            List of PageAnalysis results
        """
        analyses = []

        for i in range(0, len(pages), batch_size):
            batch = pages[i : i + batch_size]
            print(
                f"Analyzing pages {i + 1}-{min(i + batch_size, len(pages))} of {len(pages)}..."
            )

            for page in batch:
                analysis = self.analyze_page(page)
                analyses.append(analysis)

        return analyses

    def analyze_notebook_directory(
        self, notebook_dir: Path, page_pattern: str = "page_*.png"
    ) -> List[PageAnalysis]:
        """
        Analyze all pages in a notebook directory.

        Args:
            notebook_dir: Directory containing notebook page images
            page_pattern: Glob pattern for page files

        Returns:
            List of PageAnalysis results
        """
        # Find all page files
        page_files = sorted(notebook_dir.glob(page_pattern))

        if not page_files:
            raise ValueError(f"No pages found in {notebook_dir} matching {page_pattern}")

        # Create NotebookPage objects
        pages = []
        for i, page_file in enumerate(page_files, start=1):
            pages.append(NotebookPage(page_number=i, file_path=page_file))

        # Analyze all pages
        return self.analyze_pages(pages)

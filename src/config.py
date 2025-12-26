"""Configuration management for V5-Notebook-Helper."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4-vision-preview"

    # Project Paths
    project_root: Path = Path(__file__).parent.parent
    notebook_pages_dir: Path = project_root / "notebook-pages"
    data_dir: Path = project_root / "data"
    results_dir: Path = project_root / "data" / "results"

    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True

    # Analysis Settings
    max_pages_per_batch: int = 10
    analysis_temperature: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        """Initialize settings and ensure required directories exist."""
        super().__init__(**kwargs)

        # Create necessary directories
        self.data_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    @property
    def rubric_file(self) -> Path:
        """Path to rubric criteria YAML file."""
        return self.data_dir / "rubric" / "criteria.yaml"

    @property
    def questions_file(self) -> Path:
        """Path to interview questions YAML file."""
        return self.data_dir / "questions" / "questions.yaml"

    @property
    def tracking_file(self) -> Path:
        """Path to progress tracking JSON file."""
        return self.results_dir / "tracking.json"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings

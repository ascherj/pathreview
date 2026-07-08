"""Shared test fixtures for PathReview."""

from datetime import UTC, datetime

import pytest

from core.models.profile import Profile


@pytest.fixture
def sample_user_profile() -> Profile:
    """Return a sample ``Profile`` instance for testing.

    Provides a deterministic, in-memory :class:`core.models.profile.Profile`
    (not persisted to a database) populated with realistic, non-null values for
    every column on the model. Shared here so tests that need profile data can
    depend on consistent sample values instead of building ad-hoc mocks.
    """
    created = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
    return Profile(
        id="11111111-1111-4111-8111-111111111111",
        user_id="22222222-2222-4222-8222-222222222222",
        github_username="janedoe",
        resume_filename="jane_doe_resume.pdf",
        resume_text=(
            "Jane Doe — Software Engineer. Built REST APIs with Python, "
            "FastAPI, React, and PostgreSQL."
        ),
        portfolio_url="https://janedoe.dev",
        created_at=created,
        updated_at=created,
    )


@pytest.fixture
def sample_resume_text() -> str:
    """Return a sample resume text for testing."""
    return """
    Jane Doe
    Software Engineer
    jane.doe@example.com | github.com/janedoe

    Experience:
    - Software Engineer at TechCorp (2022-2024)
      Built REST APIs using Python and FastAPI.

    Education:
    - B.S. Computer Science, State University (2022)

    Skills: Python, JavaScript, React, PostgreSQL, Docker
    """


@pytest.fixture
def sample_readme_text() -> str:
    """Return a sample README text for testing."""
    return """
    # Weather App
    A weather forecasting application built with React and OpenWeatherMap API.

    ## Features
    - Current weather display
    - 5-day forecast
    - Location search

    ## Tech Stack
    - React 18
    - TypeScript
    - Tailwind CSS
    - OpenWeatherMap API
    """

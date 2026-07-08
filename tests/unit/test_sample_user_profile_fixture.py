"""Reproduction for issue #106 — missing shared `sample_user_profile` fixture.

https://github.com/jamjamgobambam/pathreview/issues/106

This test documents the gap: there is no shared `sample_user_profile` fixture
in `tests/conftest.py` (nor a `tests/fixtures/` directory). Running this test
therefore fails at collection/setup with:

    E       fixture 'sample_user_profile' not found

Once the fixture is added in the Week 9 fix, this test should pass by asserting
the fixture exposes the fields defined on `core.models.profile.Profile`.
"""

from typing import Any

import pytest


@pytest.mark.unit
def test_sample_user_profile_fixture_is_available(sample_user_profile: Any) -> None:
    """A shared sample user profile fixture should exist and expose Profile fields."""
    # These are the fields defined on core/models/profile.py::Profile.
    for field in (
        "id",
        "user_id",
        "github_username",
        "resume_filename",
        "resume_text",
        "portfolio_url",
    ):
        assert hasattr(sample_user_profile, field) or field in sample_user_profile

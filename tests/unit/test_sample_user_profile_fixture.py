"""Verification test for the shared ``sample_user_profile`` fixture (issue #106).

https://github.com/jamjamgobambam/pathreview/issues/106

Originally this test reproduced the gap — requesting the fixture raised
``fixture 'sample_user_profile' not found``. Now that the fixture exists in
``tests/conftest.py``, this test verifies it exposes every field defined on
``core.models.profile.Profile`` with the correct, non-null types.
"""

from datetime import datetime
from uuid import UUID

import pytest

from core.models.profile import Profile

PROFILE_FIELDS = (
    "id",
    "user_id",
    "github_username",
    "resume_filename",
    "resume_text",
    "portfolio_url",
    "created_at",
    "updated_at",
)


@pytest.mark.unit
def test_sample_user_profile_is_a_profile_instance(sample_user_profile: Profile) -> None:
    """The fixture returns a ``Profile`` model instance."""
    assert isinstance(sample_user_profile, Profile)


@pytest.mark.unit
def test_sample_user_profile_exposes_all_fields(sample_user_profile: Profile) -> None:
    """Every column defined on ``Profile`` is present and populated (non-null)."""
    for field in PROFILE_FIELDS:
        assert hasattr(sample_user_profile, field), f"missing field: {field}"
        assert getattr(sample_user_profile, field) is not None, f"null field: {field}"


@pytest.mark.unit
def test_sample_user_profile_ids_are_valid_uuids(sample_user_profile: Profile) -> None:
    """``id`` and ``user_id`` are valid UUID strings (matching the model column)."""
    UUID(sample_user_profile.id)
    UUID(sample_user_profile.user_id)


@pytest.mark.unit
def test_sample_user_profile_timestamps_are_timezone_aware(
    sample_user_profile: Profile,
) -> None:
    """``created_at``/``updated_at`` are timezone-aware datetimes."""
    for ts in (sample_user_profile.created_at, sample_user_profile.updated_at):
        assert isinstance(ts, datetime)
        assert ts.tzinfo is not None

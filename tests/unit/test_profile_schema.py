"""Tests for the profile API response schema.

Reproduces issue #78
(https://github.com/jamjamgobambam/pathreview/issues/78): after creating a
profile, the response schema exposes the identifier only as ``id`` and is
missing the ``profile_id`` field that clients need to make subsequent requests.
"""

from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest

from api.schemas.profile import ProfileResponse


@pytest.mark.unit
class TestProfileResponseSchema:
    """Schema-level tests for ProfileResponse (issue #78)."""

    @pytest.fixture
    def profile_row(self) -> SimpleNamespace:
        """Stand-in for a persisted Profile ORM row.

        Mirrors ``core.models.profile.Profile``: the primary key is stored as
        ``id`` and there is no ``profile_id`` attribute. ``ProfileResponse``
        uses ``from_attributes``, so it reads these attributes directly.
        """
        return SimpleNamespace(
            id=uuid4(),
            user_id=uuid4(),
            github_username="janedoe",
            portfolio_url="https://janedoe.dev",
            created_at=datetime.now(UTC),
            resume_filename="resume.pdf",
        )

    def test_response_includes_profile_id(self, profile_row: SimpleNamespace) -> None:
        """The creation response must expose a ``profile_id`` field.

        Currently FAILS (documents issue #78): ``ProfileResponse`` only defines
        ``id``, so ``profile_id`` never appears in the serialized payload.
        """
        response = ProfileResponse.model_validate(profile_row)
        payload = response.model_dump()

        assert (
            "profile_id" in payload
        ), "ProfileResponse is missing the 'profile_id' field (issue #78)"

    def test_profile_id_matches_id(self, profile_row: SimpleNamespace) -> None:
        """``profile_id`` should carry the same value as the record's ``id``."""
        response = ProfileResponse.model_validate(profile_row)
        payload = response.model_dump()

        assert payload.get("profile_id") == profile_row.id

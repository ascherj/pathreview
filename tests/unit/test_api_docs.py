"""Parity checks that docs/API.md documents POST /profiles and POST /reviews request bodies."""

from pathlib import Path

import pytest

API_MD = Path(__file__).resolve().parents[2] / "docs" / "API.md"


@pytest.mark.unit
class TestApiDocsRequestSchemas:
    """Ensure API.md keeps request body schemas for profile and review creation."""

    def _read_api_md(self) -> str:
        """Return the contents of docs/API.md."""
        return API_MD.read_text(encoding="utf-8")

    def test_api_md_documents_post_profiles_multipart_fields(self) -> None:
        """POST /profiles section documents multipart Form/File fields, not JSON."""
        content = self._read_api_md()

        assert "POST /profiles" in content
        assert "multipart/form-data" in content
        assert "github_username" in content
        assert "portfolio_url" in content
        assert "resume_file" in content
        assert "PDF" in content
        assert "Markdown" in content

    def test_api_md_documents_post_reviews_json_profile_id(self) -> None:
        """POST /reviews section documents JSON body with required profile_id UUID."""
        content = self._read_api_md()

        assert "POST /reviews" in content
        assert "application/json" in content
        assert "profile_id" in content
        assert "123e4567-e89b-12d3-a456-426614174000" in content

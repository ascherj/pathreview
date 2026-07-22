"""Unit tests for review routes."""

from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest
from fastapi import BackgroundTasks, HTTPException

from api.routes.reviews import create_review_endpoint
from api.schemas.review import ReviewCreate


class TestCreateReviewEndpoint:
    """Tests for POST /reviews."""

    @pytest.mark.asyncio
    async def test_returns_error_when_profile_has_no_ingested_documents(self) -> None:
        """The endpoint should preserve the expected no-documents error."""
        profile_id = uuid4()

        data = ReviewCreate(profile_id=profile_id)
        current_user = Mock()
        current_user.id = uuid4()

        db = AsyncMock()
        background_tasks = BackgroundTasks()

        no_documents_error = HTTPException(
            status_code=400,
            detail="Profile has no ingested documents",
        )

        with (
            patch(
                "api.routes.reviews.create_review",
                new=AsyncMock(side_effect=no_documents_error),
            ),
            pytest.raises(HTTPException) as exc_info,
        ):
            await create_review_endpoint(
                data=data,
                background_tasks=background_tasks,
                current_user=current_user,
                db=db,
            )

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Profile has no ingested documents"
        db.rollback.assert_not_awaited()

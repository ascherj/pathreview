from unittest.mock import AsyncMock
from unittest.mock import Mock
from uuid import uuid4

import pytest

from core.services.review_service import create_review


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_review_rejects_profile_owned_by_another_user():
    db = Mock()
    profile_result = Mock()
    profile_result.scalars.return_value.first.return_value = None
    db.execute = AsyncMock(return_value=profile_result)
    db.add = Mock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    result = await create_review(db, uuid4(), uuid4())

    assert result is None
    db.add.assert_not_called()
    db.commit.assert_not_awaited()
    db.refresh.assert_not_awaited()

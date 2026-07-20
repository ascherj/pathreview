"""Integration test reproducing issue #82.

process_review has no per-profile lock, so two review requests for the
same profile run fully overlapped instead of being serialized.
"""

import asyncio
import time
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest

from core.database import AsyncSessionLocal
from core.models.profile import Profile
from core.models.user import User
from core.services.review_service import create_review, process_review


@pytest.mark.integration
@pytest.mark.asyncio
async def test_concurrent_reviews_for_same_profile_are_not_serialized() -> None:
    """
    Two concurrent review requests for the same profile both start
    processing immediately, with nothing serializing the second behind
    the first.

    The agent-orchestration step is patched to take 0.3s so the overlap
    is deterministic instead of a timing-dependent race.
    """
    user_id = uuid4()
    profile_id = uuid4()

    async with AsyncSessionLocal() as db:
        db.add(User(id=str(user_id), email=f"{user_id}@example.com", hashed_password="x"))
        db.add(Profile(id=str(profile_id), user_id=str(user_id), github_username="octocat"))
        await db.commit()

    events: list[tuple[str, float]] = []

    async def slow_agent_orchestration(profile: Profile, ingestion_results: list[dict]) -> dict:
        events.append(("start", time.monotonic()))
        await asyncio.sleep(0.3)
        events.append(("end", time.monotonic()))
        return {"sections": [], "overall_score": 0.5}

    async def run_one_review() -> None:
        async with AsyncSessionLocal() as db:
            review = await create_review(db=db, profile_id=profile_id, user_id=user_id)
        async with AsyncSessionLocal() as db:
            await process_review(db=db, review_id=review.id, profile_id=profile_id)

    try:
        with patch(
            "core.services.review_service._run_agent_orchestration",
            slow_agent_orchestration,
        ):
            await asyncio.gather(run_one_review(), run_one_review())

        starts = sorted(t for label, t in events if label == "start")
        ends = sorted(t for label, t in events if label == "end")

        assert len(starts) == 2 and len(ends) == 2

        # Expected if reviews were serialized per profile: the second run
        # starts only after the first finishes. Actual today: both start
        # before either finishes, since nothing locks on profile_id.
        assert starts[1] > ends[0], (
            "Second review started processing before the first one "
            "finished -- process_review has no per-profile lock, so "
            "concurrent reviews for the same profile are never serialized "
            "(issue #82)."
        )
    finally:
        async with AsyncSessionLocal() as db:
            user = await db.get(User, str(user_id))
            if user:
                await db.delete(user)
                await db.commit()

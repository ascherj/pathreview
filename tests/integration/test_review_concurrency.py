"""Regression test for GitHub issue #82.

Concurrent review requests for the same profile can produce inconsistent
results: when a user submits two review requests for the same profile at
nearly the same time, both requests run review_service.process_review()
against the same profile_id with no synchronization. The second loop can
start (and even finish) before the first loop (which is still holding an
earlier snapshot of the profile) has released whatever exclusive access it
should have had, so results become interleaved and inconsistent.

Requires a live Postgres instance (see docker-compose.yml, port 5433) since
this exercises core/database.py's real async engine/session machinery, the
same as production. Run `docker-compose up -d postgres` before this test.
"""

import asyncio
import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import async_sessionmaker

import core.services.review_service as review_service
from core.database import engine
from core.models.profile import Profile
from core.models.review import Review
from core.models.user import User

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def _require_postgres():
    try:
        async with engine.connect():
            pass
    except (OperationalError, ConnectionError, OSError) as exc:
        pytest.skip(f"Postgres not reachable (run `docker-compose up -d postgres`): {exc}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_concurrent_reviews_for_same_profile_are_serialized():
    """Two review loops for the same profile must not run concurrently.

    Review A starts first (against resume v1), pauses mid-ingestion to
    simulate real GitHub/portfolio fetch latency. While paused, the user
    edits their profile (resume v2) and submits review B. Without a
    per-profile lock, B's loop starts & finishes while A is still
    in flight. A correct fix serializes the two loops: B must not start
    until A has fully finished (or vice versa), never interleaved.
    """
    await _require_postgres()

    call_order = []
    user_id = None
    profile_id = None
    review_id_a = None
    review_id_b = None

    original_ingest = review_service._run_ingestion_pipeline

    async def slow_ingest_a(db, profile):
        call_order.append("A_start")
        await asyncio.sleep(0.2)
        result = await original_ingest(db, profile)
        call_order.append("A_end")
        return result

    async def fast_ingest_b(db, profile):
        call_order.append("B_start")
        result = await original_ingest(db, profile)
        call_order.append("B_end")
        return result

    session_a = SessionLocal()
    session_b = SessionLocal()

    try:
        async with SessionLocal() as setup_session:
            user = User(email=f"race-{uuid.uuid4()}@example.com", hashed_password="x")
            setup_session.add(user)
            await setup_session.commit()
            await setup_session.refresh(user)
            user_id = user.id

            profile = Profile(
                user_id=user_id,
                resume_text="v1: Software Engineer with 2 years experience",
            )
            setup_session.add(profile)
            await setup_session.commit()
            await setup_session.refresh(profile)
            profile_id = profile.id

        review_a = Review(profile_id=profile_id, status="pending")
        session_a.add(review_a)
        await session_a.commit()
        await session_a.refresh(review_a)
        review_id_a = review_a.id

        review_b = Review(profile_id=profile_id, status="pending")
        session_b.add(review_b)
        await session_b.commit()
        await session_b.refresh(review_b)
        review_id_b = review_b.id

        async def process_a():
            review_service._run_ingestion_pipeline = slow_ingest_a
            await review_service.process_review(session_a, review_id_a, profile_id)

        async def process_b():
            await asyncio.sleep(0.05)
            async with SessionLocal() as edit_session:
                result = await edit_session.execute(select(Profile).where(Profile.id == profile_id))
                live_profile = result.scalars().first()
                live_profile.resume_text = "v2: Senior Software Engineer with 5 years experience"
                edit_session.add(live_profile)
                await edit_session.commit()

            review_service._run_ingestion_pipeline = fast_ingest_b
            await review_service.process_review(session_b, review_id_b, profile_id)

        await asyncio.gather(process_a(), process_b())

        # A per-profile lock must fully serialize the two loops: one loop's
        # start/end pair must not straddle the other's. Today, with no lock,
        # this produces ["A_start", "B_start", "B_end", "A_end"]. B runs
        # entirely nested inside A's still-open window.
        assert call_order in (
            ["A_start", "A_end", "B_start", "B_end"],
            ["B_start", "B_end", "A_start", "A_end"],
        ), f"expected non-interleaved execution, got {call_order}"

    finally:
        review_service._run_ingestion_pipeline = original_ingest
        await session_a.close()
        await session_b.close()

        async with SessionLocal() as cleanup_session:
            if review_id_a is not None:
                await cleanup_session.execute(
                    Review.__table__.delete().where(Review.id.in_([review_id_a, review_id_b]))
                )
            if profile_id is not None:
                await cleanup_session.execute(
                    Profile.__table__.delete().where(Profile.id == profile_id)
                )
            if user_id is not None:
                await cleanup_session.execute(User.__table__.delete().where(User.id == user_id))
            await cleanup_session.commit()

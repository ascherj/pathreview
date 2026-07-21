from uuid import UUID
import structlog
from sqlalchemy import select

from core.models.profile import Profile
from core.models.review import Review
from core.models.ingested_source import IngestedSource
from api.schemas.profile import ProfileCreate, ProfileUpdate

log = structlog.get_logger()


async def create_profile(
    db,
    user_id: UUID,
    data: ProfileCreate,
    resume_filename: str = None,
    resume_text: str = None,
) -> Profile:
    """Create a new profile for a user.

    Args:
        db: Database session.
        user_id: UUID of the owning user.
        data: Profile creation payload.
        resume_filename: Optional uploaded resume filename.
        resume_text: Optional uploaded resume text content.

    Returns:
        The newly created Profile.

    Raises:
        sqlalchemy.exc.IntegrityError: If a profile with the same user_id
            already exists.
    """
    profile = Profile(
        user_id=user_id,
        github_username=data.github_username,
        portfolio_url=data.portfolio_url,
        resume_filename=resume_filename,
        resume_text=resume_text,
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_profile(
    db,
    profile_id: UUID,
    user_id: UUID,
) -> Profile | None:
    """Get a profile by ID, checking ownership.

    Args:
        db: Database session.
        profile_id: UUID of the profile to retrieve.
        user_id: UUID of the requesting user (ownership check).

    Returns:
        The Profile if found and owned by user_id, otherwise None.
    """
    stmt = select(Profile).where(
        (Profile.id == profile_id) & (Profile.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_profile(
    db,
    profile_id: UUID,
    user_id: UUID,
    data: ProfileUpdate,
) -> Profile | None:
    """Update a profile, checking ownership.

    Args:
        db: Database session.
        profile_id: UUID of the profile to update.
        user_id: UUID of the requesting user (ownership check).
        data: Profile update payload with optional fields.

    Returns:
        The updated Profile if found and owned, otherwise None.
    """
    profile = await get_profile(db, profile_id, user_id)
    if not profile:
        return None

    if data.github_username is not None:
        profile.github_username = data.github_username
    if data.portfolio_url is not None:
        profile.portfolio_url = data.portfolio_url

    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_profile(
    db,
    profile_id: UUID,
    user_id: UUID,
) -> bool:
    """Delete a profile and cascade delete its reviews and ingested sources.

    Args:
        db: Database session.
        profile_id: UUID of the profile to delete.
        user_id: UUID of the requesting user (ownership check).

    Returns:
        True if the profile was deleted, False if not found.

    Raises:
        Exception: If the database cascade operation fails; the transaction
            is rolled back.
    """
    profile = await get_profile(db, profile_id, user_id)
    if not profile:
        return False

    try:
        # Delete related reviews
        stmt = select(Review).where(Review.profile_id == profile_id)
        result = await db.execute(stmt)
        reviews = result.scalars().all()
        for review in reviews:
            await db.delete(review)

        # Delete related ingested sources
        stmt = select(IngestedSource).where(IngestedSource.profile_id == profile_id)
        result = await db.execute(stmt)
        sources = result.scalars().all()
        for source in sources:
            await db.delete(source)

        # Delete profile
        await db.delete(profile)
        await db.commit()

        log.info("profile_deleted_cascade", profile_id=str(profile_id))
        return True

    except Exception as exc:
        log.error("profile_cascade_delete_failed", profile_id=str(profile_id), error=str(exc))
        await db.rollback()
        raise

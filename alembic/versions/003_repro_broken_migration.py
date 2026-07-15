"""REPRODUCTION (issue #129): deliberately broken migration.

This migration renames reviews.error_message -> reviews.error_detail.
The SQLAlchemy model (core/models/review.py) still declares `error_message`,
so after this migration the live schema DRIFTS from the models.

It is syntactically valid Python, so it passes ruff, black, and mypy, and
the test suite never applies migrations -- so nothing in CI catches it today.
This file exists only to document the reproduced gap and should be removed
once the migration-validation step is added.

Revision ID: 003
Revises: 002
Create Date: 2026-07-15 00:00:00.000000
"""

from alembic import op  # type: ignore[attr-defined]

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drift: the model still calls this column `error_message`.
    op.alter_column("reviews", "error_message", new_column_name="error_detail")


def downgrade() -> None:
    op.alter_column("reviews", "error_detail", new_column_name="error_message")

"""Tests for health.py"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import HTTPException
from api.routes.health import health_check


@pytest.mark.unit
class TestHealthCheck:
    """Test suite for the health check endpoint."""

    @pytest.mark.asyncio
    @patch("redis.Redis.from_url")
    async def test_health_check_healthy(self, mock_redis_from_url):
        """Test health check returns healthy when all dependencies are healthy."""
        # Mock database session
        mock_db = AsyncMock()
        mock_db.execute.return_value = None

        # Mock Redis client
        mock_redis = Mock()
        mock_redis.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis

        # Mock Settings
        with patch("core.config.settings") as mock_settings:
            mock_settings.redis_url = "redis://localhost:6379/0"
            mock_settings.vector_db_url = "http://localhost:8001"

            response = await health_check(db=mock_db)

            assert response["status"] == "healthy"
            assert response["dependencies"]["postgres"] == "healthy"
            assert response["dependencies"]["redis"] == "healthy"
            assert response["dependencies"]["vector_db"] == "healthy"
            mock_db.execute.assert_called_once()
            mock_redis_from_url.assert_called_once_with(
                "redis://localhost:6379/0", decode_responses=True
            )

    @pytest.mark.asyncio
    @patch("redis.Redis.from_url")
    async def test_health_check_unhealthy_postgres(self, mock_redis_from_url):
        """Test health check returns unhealthy and raises 503 when Postgres is down."""
        # Mock database session to raise error
        mock_db = AsyncMock()
        mock_db.execute.side_effect = Exception("DB Connection Refused")

        # Mock Redis client
        mock_redis = Mock()
        mock_redis.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis

        # Mock Settings
        with patch("core.config.settings") as mock_settings:
            mock_settings.redis_url = "redis://localhost:6379/0"
            mock_settings.vector_db_url = "http://localhost:8001"

            with pytest.raises(HTTPException) as exc_info:
                await health_check(db=mock_db)

            assert exc_info.value.status_code == 503
            assert exc_info.value.detail["status"] == "unhealthy"
            assert exc_info.value.detail["dependencies"]["postgres"] == "unhealthy"
            assert exc_info.value.detail["dependencies"]["redis"] == "healthy"

    @pytest.mark.asyncio
    @patch("redis.Redis.from_url")
    async def test_health_check_unhealthy_redis(self, mock_redis_from_url):
        """Test health check returns unhealthy and raises 503 when Redis is down."""
        # Mock database session
        mock_db = AsyncMock()
        mock_db.execute.return_value = None

        # Mock Redis client to raise error
        mock_redis_from_url.side_effect = Exception("Redis Connection Refused")

        # Mock Settings
        with patch("core.config.settings") as mock_settings:
            mock_settings.redis_url = "redis://localhost:6379/0"
            mock_settings.vector_db_url = "http://localhost:8001"

            with pytest.raises(HTTPException) as exc_info:
                await health_check(db=mock_db)

            assert exc_info.value.status_code == 503
            assert exc_info.value.detail["status"] == "unhealthy"
            assert exc_info.value.detail["dependencies"]["postgres"] == "healthy"
            assert exc_info.value.detail["dependencies"]["redis"] == "unhealthy"

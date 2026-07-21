# from fastapi import Request
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.responses import Response
from starlette.responses import Response, JSONResponse
import uuid
import structlog

from safety.rate_limiter import RateLimiter

log = structlog.get_logger()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that generates a unique request ID for each incoming request,
    attaches it to the request state, and adds it to response headers.
    Also binds the request_id to structlog context for the duration of the request.
    """
    def __init__(self, app, rate_limiter: RateLimiter):
        super().__init__(app)
        self.limiter = rate_limiter
        self.limit = 60
        self.window_seconds = 60

    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Attach to request state
        request.state.request_id = request_id

        # Bind to structlog context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        client_ip = request.client.host if request.client else "unknown"

        allowed, remaining = self.limiter.check_rate_limit(
            identifier=client_ip,
            limit=self.limit,
            window_seconds=self.window_seconds
        )

        if not allowed:
            log.warning("rate_limit_blocked", client_ip=client_ip, limit=self.limit)
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Try again later."}
            )
        else:

            # Process request
            response = await call_next(request)

        # Add request ID to response header
        response.headers["X-Request-ID"] = request_id
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

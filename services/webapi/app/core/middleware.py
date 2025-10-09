"""Custom middleware for the application."""

import time
from collections.abc import Callable

from fastapi import FastAPI, Request, Response


def add_middleware(app: FastAPI) -> None:
    """Add custom middleware to the FastAPI application."""

    @app.middleware("http")
    async def add_process_time_header(
        request: Request, call_next: Callable
    ) -> Response:
        """Add processing time to response headers."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next: Callable) -> Response:
        """Add security headers to responses."""
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

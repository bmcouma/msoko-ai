"""
Msoko AI Middleware
===================
Phase 1 Observability: Tracks AI usage metadata per request/user.
The actual AI call logging happens in chatbot/utils/agent.py using
the `msoko.ai_usage` logger. This middleware tracks request-level
metadata (endpoint, user, latency) and logs it to the same logger.
"""

import time
import logging

logger = logging.getLogger("msoko.ai_usage")

_AI_ENDPOINTS = {"/api/stream/", "/api/chat/"}


class AIUsageMiddleware:
    """
    Lightweight middleware that:
    1. Detects AI endpoint requests.
    2. Records wall-clock latency.
    3. Logs user + endpoint + latency for audit/observability.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Only instrument AI endpoints — skip everything else
        if path not in _AI_ENDPOINTS:
            return self.get_response(request)

        start = time.monotonic()
        response = self.get_response(request)
        latency_ms = (time.monotonic() - start) * 1000

        user_id = request.user.id if request.user.is_authenticated else "anonymous"
        username = request.user.username if request.user.is_authenticated else "anon"

        logger.info(
            f"endpoint={path} user_id={user_id} username={username} "
            f"status={response.status_code} latency_ms={latency_ms:.1f}"
        )

        return response

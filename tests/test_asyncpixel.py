"""Main tests."""
import asyncio

import pytest
import random

from asyncpixel import __version__, Client
from tests.aiohttp import CaseControlledTestServer, http_redirect
from tests.certificate import ssl_certificate, TemporaryCertificate  # noqa: F401

TIMEOUT = 1


def test_version() -> None:
    """Mock version."""
    assert __version__ == "1.0.0"


@pytest.mark.asyncio
async def test_key(http_redirect):  # noqa: F401
    async with CaseControlledTestServer() as server:
        http_redirect.add_server("api.hypixel.net", 80, server.port)
        client = Client(session=http_redirect.session)

        task = asyncio.ensure_future(client.api_key("Lord_Ewout"))
        request = await server.receive_request(timeout=TIMEOUT)
        assert request.path_qs == "/key"

        key = "e1513542-f4c7-483d-bf1b-3b29d4e59903"
        owner = "8ffb79fa-620e-45fe-8d62-381abd5bc60f"
        limit = random.randint(120, 1000)
        queries_in_past_min = random.randint(0, 120)
        total_queries = random.randint(100, 1000)

        server.send_response(
            request,
            text={
                "success": True,
                "record": {
                    "key": key,
                    "owner": owner,
                    "limit": limit,
                    "queriesInPastMin": queries_in_past_min,
                    "totalQueries": total_queries,
                },
            },
            content_type="application/json",
        )
        result = await asyncio.wait_for(task, TIMEOUT)
        assert result.key == key
        assert result.owner == owner
        assert result.limit == limit
        assert result.queriesInPastMin == queries_in_past_min
        assert result.totalQueries == total_queries

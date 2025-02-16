import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Create a session-scoped event loop for all tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
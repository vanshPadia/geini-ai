import pytest
from httpx import ASGITransport, AsyncClient

from app import create_app


@pytest.fixture(scope='package')
def client():
    client = AsyncClient(
        transport=ASGITransport(
            app=create_app()
        )
    )

    return client

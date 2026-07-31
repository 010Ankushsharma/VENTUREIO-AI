"""
Auth tests.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "pass123", "full_name": "Test User"},
    )
    assert response.status_code == 201
    assert "access_token" in response.json()

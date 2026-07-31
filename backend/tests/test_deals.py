"""
Deal tests.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_deal(client: AsyncClient):
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "a@b.com", "password": "pass123", "full_name": "Test"},
    )
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        "/api/v1/deals/",
        json={"name": "Test Startup", "industry": "FinTech", "stage": "Seed"},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Startup"

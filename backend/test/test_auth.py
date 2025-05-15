import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(loop_scope="session")

async def test_admin_creates_and_logs_in_user(client: AsyncClient):
    login = await client.post(
        "/auth/token",
        data={"username": "admin@example.com", "password": "adminpass"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post(
        "/users/",
        json={
            "email": "alice@example.com",
            "full_name": "Alice",
            "password": "secret123"
        },
        headers=headers
    )
    assert r.status_code == 201

    login2 = await client.post(
        "/auth/token",
        data={"username": "alice@example.com", "password": "secret123"},
    )
    assert login2.status_code == 200
    body = login2.json()
    assert "access_token" in body and body["token_type"] == "bearer"


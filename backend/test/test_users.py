import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_user_crud(client: AsyncClient):

    r = await client.post("/auth/token", data={
        "username": "admin@example.com", "password": "adminpass"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    
    r = await client.post("/users/", json={
        "email": "bob@example.com",
        "full_name": "Bob",
        "password": "hunter2"
    }, headers=headers)
    assert r.status_code == 201
    user = r.json()

    r = await client.get("/users/", headers=headers)
    assert r.status_code == 200
    assert any(u["email"] == "bob@example.com" for u in r.json())

    r = await client.patch(f"/users/{user['id']}", json={
        "full_name": "Bobby"
    }, headers=headers)
    assert r.json()["full_name"] == "Bobby"

    r = await client.delete(f"/users/{user['id']}", headers=headers)
    assert r.status_code == 204

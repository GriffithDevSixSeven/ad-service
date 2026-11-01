"""User endpoint tests."""

from httpx import AsyncClient


async def test_create_user(client: AsyncClient):
    payload = {"user_name": "john", "email": "john@example.com", "password": "secret"}
    response = await client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_name"] == "john"
    assert data["email"] == "john@example.com"
    assert "id" in data


async def test_get_user(client: AsyncClient):
    payload = {"user_name": "jane", "email": "jane@example.com", "password": "secret"}
    created = await client.post("/users", json=payload)
    user_id = created.json()["id"]
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_name"] == "jane"


async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/users/999")
    assert response.status_code == 404


async def test_update_user(client: AsyncClient):
    payload = {"user_name": "bob", "email": "bob@example.com", "password": "secret"}
    created = await client.post("/users", json=payload)
    user_id = created.json()["id"]
    response = await client.patch(f"/users/{user_id}", json={"user_name": "bobby"})
    assert response.status_code == 200
    assert response.json()["user_name"] == "bobby"


async def test_delete_user(client: AsyncClient):
    payload = {"user_name": "del", "email": "del@example.com", "password": "secret"}
    created = await client.post("/users", json=payload)
    user_id = created.json()["id"]
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 404

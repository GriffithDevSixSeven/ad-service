"""Ad endpoint tests."""

from httpx import AsyncClient


async def _create_user(client: AsyncClient) -> int:
    payload = {"user_name": "owner", "email": "owner@example.com", "password": "secret"}
    response = await client.post("/users", json=payload)
    return response.json()["id"]


async def test_create_ad(client: AsyncClient):
    owner_id = await _create_user(client)
    payload = {
        "title": "Bike",
        "category": "transport",
        "price": 100.5,
        "name": "Giant",
        "owner_id": owner_id,
    }
    response = await client.post("/ads", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Bike"
    assert data["owner_id"] == owner_id


async def test_list_ads_paginated(client: AsyncClient):
    owner_id = await _create_user(client)
    for i in range(3):
        await client.post(
            "/ads",
            json={
                "title": f"Ad {i}",
                "category": "cat",
                "price": 10.0,
                "name": f"name{i}",
                "owner_id": owner_id,
            },
        )
    response = await client.get("/ads", params={"page": 1, "page_size": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2


async def test_get_ad_not_found(client: AsyncClient):
    response = await client.get("/ads/999")
    assert response.status_code == 404


async def test_update_ad(client: AsyncClient):
    owner_id = await _create_user(client)
    created = await client.post(
        "/ads",
        json={
            "title": "Old",
            "category": "cat",
            "price": 5.0,
            "name": "n",
            "owner_id": owner_id,
        },
    )
    ad_id = created.json()["id"]
    response = await client.patch(f"/ads/{ad_id}", json={"title": "New"})
    assert response.status_code == 200
    assert response.json()["title"] == "New"


async def test_delete_ad(client: AsyncClient):
    owner_id = await _create_user(client)
    created = await client.post(
        "/ads",
        json={
            "title": "Del",
            "category": "cat",
            "price": 5.0,
            "name": "n",
            "owner_id": owner_id,
        },
    )
    ad_id = created.json()["id"]
    response = await client.delete(f"/ads/{ad_id}")
    assert response.status_code == 204
    response = await client.get(f"/ads/{ad_id}")
    assert response.status_code == 404

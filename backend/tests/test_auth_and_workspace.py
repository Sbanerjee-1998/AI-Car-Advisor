from backend.tests.factories import register_payload


def test_register_me_logout_and_login(client):
    response = client.post("/api/auth/register", json=register_payload("Asha@Example.com"))
    assert response.status_code == 201
    assert response.json()["email"] == "asha@example.com"
    assert client.get("/api/auth/me").status_code == 200

    chat = client.post("/api/chats", json={"title": "Family car search"})
    assert chat.status_code == 201
    chat_id = chat.json()["id"]

    assert client.post("/api/auth/logout").status_code == 204
    assert client.get("/api/auth/me").status_code == 401
    assert client.post("/api/auth/login", json={"email": "ASHA@example.com", "password": "correct horse"}).status_code == 200
    assert chat_id in {item["id"] for item in client.get("/api/chats").json()["items"]}


def test_duplicate_and_invalid_credentials_are_safe(client):
    assert client.post("/api/auth/register", json=register_payload()).status_code == 201
    duplicate = client.post("/api/auth/register", json=register_payload(" DRIVER@example.com "))
    assert duplicate.status_code == 409
    assert duplicate.json() == {"error": {"code": "conflict", "message": "An account with that email already exists.", "fields": None}}
    invalid = client.post("/api/auth/login", json={"email": "driver@example.com", "password": "wrong password"})
    assert invalid.status_code == 401
    assert "password_hash" not in invalid.text


def test_chat_and_private_resources_are_owned(registered_client):
    chat = registered_client.post("/api/chats", json={})
    assert chat.status_code == 201
    chat_id = chat.json()["id"]
    message = registered_client.post(f"/api/chats/{chat_id}/messages", json={"content": "I need an automatic petrol family SUV under 15 lakh"})
    assert message.status_code == 200
    body = message.json()
    assert body["conversation_id"] == chat_id
    assert len(body["recommendations"]) <= 3
    assert body["disclaimer"]
    assert registered_client.get("/api/chats").json()["items"][0]["id"] == chat_id
    assert registered_client.get("/api/cars").status_code == 200
    assert registered_client.get("/api/cars/maruti-brezza").status_code == 200


def test_favourites_and_compare(registered_client):
    save = registered_client.post("/api/favourites", json={"vehicle_id": "maruti-brezza"})
    assert save.status_code == 201
    assert registered_client.get("/api/favourites").json()["items"][0]["vehicle_id"] == "maruti-brezza"
    comparison = registered_client.post("/api/compare", json={"vehicle_ids": ["maruti-brezza", "hyundai-venue"]})
    assert comparison.status_code == 200
    assert len(comparison.json()["vehicles"]) == 2
    assert registered_client.delete("/api/favourites/maruti-brezza").status_code == 204


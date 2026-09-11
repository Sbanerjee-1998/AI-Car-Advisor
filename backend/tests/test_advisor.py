from backend.app.schemas.advisor import GeminiAdvisorResponse


class FakeProvider:
    configured = True

    def generate(self, **kwargs):
        return GeminiAdvisorResponse(
            answer="This answer came from the configured AI provider.",
            recommendation_ids=[kwargs["candidates"][0]["id"], "not-in-catalog"],
        )


def test_configured_advisor_uses_ai_response_and_validates_vehicle_ids(app, registered_client):
    app.state.advisor.provider = FakeProvider()
    chat = registered_client.post("/api/chats", json={}).json()

    response = registered_client.post(
        f"/api/chats/{chat['id']}/messages",
        json={"content": "Find me a practical city car"},
    )

    assert response.status_code == 200
    body = response.json()
    assert (
        body["assistant_message"]["content"] == "This answer came from the configured AI provider."
    )
    assert len(body["recommendations"]) == 1
    assert body["recommendations"][0]["vehicle_id"] != "not-in-catalog"

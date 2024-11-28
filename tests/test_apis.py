from httpx import ASGITransport


async def test_chat_api(client: ASGITransport):
    response = await client.post('http://127.0.0.1:8000/chat', json={
        "message": "Hi, I am looking a flight from Delhi to Mumbai.",
        "user_details": {
            "user_id": "1",
            "thread_id": "101"
        },
        "state": None
    })

    assert response.status_code == 200

    response_data = response.json()
    result = response_data["result"]

    assert result["message_category"] == "TRAVEL"
    result = response_data["result"]

from app.app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_returns_message_and_hostname():
    client = app.test_client()
    data = client.get("/").get_json()
    assert "message" in data
    assert "hostname" in data

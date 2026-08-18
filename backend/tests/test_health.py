def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_provider_status_endpoint(client):
    response = client.get("/api/providers/status")
    assert response.status_code == 200
    data = response.json()
    assert "active_provider" in data
    assert "is_mock" in data

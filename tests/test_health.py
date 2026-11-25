
def test_health_endpoint(client):
    """The health endpoint should report that the app is running."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_endpoint(client):
    """The readiness endpoint should report application readiness."""

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

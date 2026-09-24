from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Test that /health returns 200 and does not require a database connection.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_metrics_endpoint():
    """Test that /metrics returns Prometheus text format."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

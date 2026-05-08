from fastapi.testclient import TestClient

from app.db import SEED_CLIENTS
from app.main import app

client = TestClient(app)


def test_get_clients_returns_expected_payload() -> None:
    response = client.get("/clients")

    assert response.status_code == 200
    assert response.json() == SEED_CLIENTS

from fastapi.testclient import TestClient

from app.main import CUSTOMERS, app

client = TestClient(app)


def test_get_customers_returns_expected_payload() -> None:
    response = client.get("/customers")

    assert response.status_code == 200
    assert response.json() == [customer.model_dump() for customer in CUSTOMERS]

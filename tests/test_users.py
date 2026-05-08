from fastapi.testclient import TestClient

from app.main import USERS, app

client = TestClient(app)


def test_get_users_returns_expected_payload() -> None:
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [user.model_dump() for user in USERS]

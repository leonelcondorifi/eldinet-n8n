import pytest
from fastapi.testclient import TestClient

from app.db import SEED_USERS
from app.main import app


@pytest.fixture(autouse=True)
def _use_tmp_db(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ELDINET_DB_PATH", str(tmp_path / "test.db"))

client = TestClient(app)


def test_get_users_returns_expected_payload() -> None:
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == SEED_USERS

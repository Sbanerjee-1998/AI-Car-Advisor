from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.main import create_app


@pytest.fixture
def app(tmp_path: Path):
    return create_app(database_url=f"sqlite:///{tmp_path / 'test.db'}", catalog_dir="backend/data/cars")


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def registered_client(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Asha Rao", "email": "asha@example.com", "password": "correct horse", "password_confirmation": "correct horse"},
    )
    assert response.status_code == 201
    return client

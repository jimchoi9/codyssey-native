"""Fixtures shared by subsequent API tests."""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    with TestClient(app, raise_server_exceptions=False) as instance:
        yield instance

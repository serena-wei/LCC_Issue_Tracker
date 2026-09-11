"""Shared pytest fixtures for Flask app tests."""
import pytest

from app import create_app
from app.config import Config


@pytest.fixture
def app():
    flask_app = create_app(Config)
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, username, password):
    """POST /login and return the response (no follow)."""
    return client.post(
        '/login',
        data={'username': username, 'password': password},
        follow_redirects=False,
    )

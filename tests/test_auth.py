"""Authentication behaviour that is easy to get wrong."""
from unittest.mock import patch

from tests.conftest import login


def test_login_success_redirects_visitor_home(client):
    response = login(client, 'visitor1', 'Visitor1pass*')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/visitor/home')


def test_login_wrong_password_stays_on_login(client):
    response = login(client, 'visitor1', 'WrongPass1*')
    assert response.status_code == 200
    assert b'password' in response.data.lower()


def test_login_inactive_user_is_blocked(client):
    inactive_account = {
        'user_id': 999,
        'username': 'inactive_user',
        'password_hash': 'unused',
        'role': 'visitor',
        'status': 'inactive',
    }
    with patch('app.blueprints.auth.users_repo.find_by_username', return_value=inactive_account):
        response = login(client, 'inactive_user', 'AnyPass1*')

    assert response.status_code == 200
    assert b'inactive' in response.data.lower()

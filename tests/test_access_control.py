"""Role-based access control for protected admin surfaces."""
from tests.conftest import login


def test_unauthenticated_issues_redirects_to_login(client):
    response = client.get('/issues?status=unresolved', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')


def test_visitor_cannot_access_user_list(client):
    login(client, 'visitor1', 'Visitor1pass*')
    response = client.get('/userlist')
    assert response.status_code == 403
    assert b'Access Denied' in response.data


def test_admin_can_access_user_list(client):
    login(client, 'admin1', 'Admin1pass*')
    response = client.get('/userlist')
    assert response.status_code == 200
    assert b'visitor1' in response.data

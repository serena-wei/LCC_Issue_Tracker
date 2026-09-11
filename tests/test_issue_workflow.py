"""Issue/comment workflow rules that encode business behaviour."""
from app import constants, db
from app.repositories import issues as issues_repo
from tests.conftest import login


def _latest_issue_id():
    with db.get_cursor() as cursor:
        cursor.execute('SELECT issue_id FROM issues ORDER BY issue_id DESC LIMIT 1;')
        row = cursor.fetchone()
        return row['issue_id']


def _issue_status(issue_id):
    with db.get_cursor() as cursor:
        cursor.execute('SELECT status FROM issues WHERE issue_id = %s;', (issue_id,))
        return cursor.fetchone()['status']


def test_visitor_only_sees_own_unresolved_issues(client, app):
    login(client, 'visitor1', 'Visitor1pass*')
    response = client.get('/issues?status=unresolved')
    assert response.status_code == 200

    with app.app_context():
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s;', ('visitor1',))
            visitor_id = cursor.fetchone()['user_id']

        own_issues = issues_repo.list_for_role(
            constants.USER_ROLE_VISITOR, visitor_id, 'unresolved')
        all_unresolved = issues_repo.list_for_role(
            constants.USER_ROLE_ADMIN, visitor_id, 'unresolved')

    assert len(own_issues) >= 1
    assert len(all_unresolved) > len(own_issues)


def test_helper_comment_reopens_issue(client, app):
    login(client, 'visitor1', 'Visitor1pass*')
    create_response = client.post(
        '/issues/insert',
        data={
            'summary': 'Pytest reopen check',
            'description': 'Created by automated test',
            'status': 'unresolved',
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 302

    with app.app_context():
        issue_id = _latest_issue_id()
        issues_repo.update_status(issue_id, constants.ISSUES_STATUS_NEW)
        assert _issue_status(issue_id) == constants.ISSUES_STATUS_NEW

    client.get('/logout')
    login(client, 'helper1', 'Helper1pass*')
    comment_response = client.post(
        '/comments/insert',
        data={
            'issue_id': str(issue_id),
            'status': 'unresolved',
            'content': 'Helper follow-up from pytest',
        },
        follow_redirects=False,
    )
    assert comment_response.status_code == 302

    with app.app_context():
        assert _issue_status(issue_id) == constants.ISSUES_STATUS_OPEN

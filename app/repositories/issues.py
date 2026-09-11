"""Issue table data access."""
from app import constants, db


def list_for_role(role, user_id, status):
    """
    Return issues for the given role and status filter.

    Visitors only see their own issues; helpers/admins see all.
    """
    with db.get_cursor() as cursor:
        if role == constants.USER_ROLE_VISITOR:
            if status == constants.ISSUES_STATUS_RESOLVED:
                cursor.execute(
                    'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status = %s;',
                    (user_id, constants.ISSUES_STATUS_RESOLVED))
            else:
                cursor.execute(
                    'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status != %s;',
                    (user_id, constants.ISSUES_STATUS_RESOLVED))
        else:
            if status == constants.ISSUES_STATUS_RESOLVED:
                cursor.execute(
                    'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status = %s;',
                    (constants.ISSUES_STATUS_RESOLVED,))
            else:
                cursor.execute(
                    'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status != %s;',
                    (constants.ISSUES_STATUS_RESOLVED,))
        return cursor.fetchall()


def create(summary, description, user_id):
    """Insert a new issue with status new."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'INSERT INTO issues (summary, description, user_id, status) VALUES (%s, %s, %s, %s);',
            (summary, description, user_id, constants.ISSUES_STATUS_NEW))


def update_status(issue_id, new_status):
    """Update an issue's status."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'UPDATE issues SET status = %s WHERE issue_id = %s;',
            (new_status, issue_id))

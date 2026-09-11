"""Comment table data access."""
from app import db


def list_for_issue(issue_id):
    """Return comments for an issue, including author profile fields."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'SELECT c.comment_id, c.content, c.created_at, u.username, u.profile_image, u.role '
            'FROM comments c '
            'LEFT JOIN users u on u.user_id = c.user_id '
            'WHERE c.issue_id = %s;',
            (issue_id,))
        return cursor.fetchall()


def create(issue_id, user_id, content):
    """Insert a new comment."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'INSERT INTO comments (issue_id, user_id, content) VALUES (%s, %s, %s);',
            (issue_id, user_id, content))

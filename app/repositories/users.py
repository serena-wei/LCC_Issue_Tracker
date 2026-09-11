"""User table data access."""
from app import constants, db


def find_by_username(username):
    """Return a user row by username, or None."""
    with db.get_cursor() as cursor:
        cursor.execute(
            '''
            SELECT user_id, username, password_hash, role, status
            FROM users
            WHERE username = %s;
            ''',
            (username,))
        return cursor.fetchone()


def find_auth_by_username(username):
    """Return user_id and password_hash for password reset, or None."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'SELECT user_id, password_hash FROM users WHERE username = %s;',
            (username,))
        return cursor.fetchone()


def username_exists(username):
    """Return True if a user with this username already exists."""
    with db.get_cursor() as cursor:
        cursor.execute('SELECT user_id FROM users WHERE username = %s;', (username,))
        return cursor.fetchone() is not None


def create_user(username, password_hash, email, first_name, last_name, location):
    """Insert a new visitor account with the default profile image."""
    with db.get_cursor() as cursor:
        cursor.execute(
            '''
            INSERT INTO users (username, password_hash, email, first_name, last_name, location, role, profile_image, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''',
            (username, password_hash, email, first_name, last_name, location,
             constants.USER_ROLE_VISITOR,
             constants.STATIC_IMAGES_URL + constants.DEFAULT_PROFILE_IMAGE_NAME,
             constants.USER_STATUS_ACTIVE))


def update_password_hash(user_id, password_hash):
    """Update a user's password hash."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'UPDATE users SET password_hash=%s WHERE user_id = %s;',
            (password_hash, user_id))


def list_all_ordered_by_status():
    """Return all users ordered by status."""
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM users ORDER BY status;')
        return cursor.fetchall()


def update_status_for_ids(user_ids, status):
    """Batch-update status for the given user IDs."""
    placeholders = ', '.join(['%s'] * len(user_ids))
    with db.get_cursor() as cursor:
        cursor.execute(
            f'UPDATE users SET status = %s WHERE user_id IN ({placeholders});',
            [status] + list(user_ids))


def update_role(user_id, role):
    """Update a single user's role."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'UPDATE users SET role = %s WHERE user_id = %s;',
            [role, user_id])


def get_profile(user_id):
    """Return profile fields for a user, or None."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'SELECT username, email, role, first_name, last_name, location, profile_image FROM users WHERE user_id = %s;',
            (user_id,))
        return cursor.fetchone()


def update_profile(user_id, email, first_name, last_name, location, profile_image):
    """Update profile fields for a user."""
    with db.get_cursor() as cursor:
        cursor.execute(
            'UPDATE users SET email=%s, first_name=%s, last_name=%s, location=%s, profile_image=%s WHERE user_id = %s;',
            (email, first_name, last_name, location, profile_image, user_id))

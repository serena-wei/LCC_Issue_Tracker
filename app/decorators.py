"""
Authentication and authorization decorators for Flask views.
Enforces login and role-based access control across the application.
"""
from functools import wraps
from flask import redirect, url_for, session, render_template
from app import constants

def login_required(f):
    """Redirects to the login page if the user is not logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if constants.SESSION_LOGGED_IN not in session:
            return redirect(url_for(constants.URL_LOGIN))
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """
    Ensures the user is logged in and has the required role.

    Args:
        required_role (str): The role required to access the view.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if constants.SESSION_LOGGED_IN not in session:
                return redirect(url_for(constants.URL_LOGIN))
            elif session.get(constants.USER_ROLE) != required_role:
                return render_template(constants.TEMPLATE_ACCESS_DENIED), constants.HTTP_STATUS_CODE_403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_and_role_required(allowed_roles):
    """
    Ensures the user is logged in and has one of the allowed roles.

    Args:
        allowed_roles (list): Roles allowed to access the view.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if constants.SESSION_LOGGED_IN not in session:
                return redirect(url_for(constants.URL_LOGIN))
            elif session.get(constants.USER_ROLE) not in allowed_roles:
                return render_template(constants.TEMPLATE_ACCESS_DENIED), constants.HTTP_STATUS_CODE_403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def if_logged_in_redirect(f):
    """Redirects already-logged-in users to their role homepage."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Late import to avoid circular dependency with app.user
        from app.user import user_home_url
        if constants.SESSION_LOGGED_IN in session:
            return redirect(user_home_url())
        return f(*args, **kwargs)
    return decorated_function

"""
auth_decorators.py

This module defines authentication and authorization decorators for 
Flask views. These decorators help enforce login and role-based access 
control across the application.
"""
from functools import wraps
from flask import redirect, url_for, session, render_template
from app import constants

def login_required(f):
    """
    Checks if the user is logged in. If not, redirects to the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if constants.SESSION_LOGGED_IN not in session:
            return redirect(url_for(constants.URL_LOGIN))
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """
    A decorator to ensure the user is logged in and has the required role.
    
    Args:
        required_role (str): The role that the user must have to access the view.
    
    Returns:
        A redirect to the login page if the user is not logged in or does not have the required role.
        If the user has the required role, it allows access to the view.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if constants.SESSION_LOGGED_IN not in session:
                # The user is not logged in, redirect to login page
                return redirect(url_for(constants.URL_LOGIN))
            elif session.get(constants.USER_ROLE) != required_role:
                # The user does not have the required role, access denied
                return render_template(constants.TEMPLATE_ACCESS_DENIED), constants.HTTP_STATUS_CODE_403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_and_role_required(allowed_roles):
    """
    A decorator to ensure the user is logged in and has one of the allowed roles.
    
    Args:
        allowed_roles (list): A list of roles that are allowed to access the view.
    
    Returns:
        A redirect to the login page if the user is not logged in or does not have one of the allowed roles.
        If the user passes the checks, the view function is called.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if constants.SESSION_LOGGED_IN not in session:
                # The user is not logged in, redirect to login page
                return redirect(url_for(constants.URL_LOGIN))
            elif session.get(constants.USER_ROLE) not in allowed_roles:
                # The user does not have the required role(s), access denied
                return render_template(constants.TEMPLATE_ACCESS_DENIED), constants.HTTP_STATUS_CODE_403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def if_logged_in_redirect(f):
    """
    Decorator to redirect users to the home page if they are already logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Import the `user_home_url` function from the `app.user` module
        # to handle redirection for users who are already logged in.
        from app.user import user_home_url
        if constants.SESSION_LOGGED_IN in session:
            # Redirect to the user home page if already logged in
            return redirect(user_home_url())  # You should define the `user_home_url()` function or the URL
        return f(*args, **kwargs)
    return decorated_function
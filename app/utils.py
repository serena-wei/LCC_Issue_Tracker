"""Small shared helpers used across blueprints."""
from flask import session, url_for

from app import constants


def user_home_url():
    """Returns the homepage URL for the current user, or the login URL if not logged in."""
    role = session.get(constants.USER_ROLE, None)

    if role == constants.USER_ROLE_VISITOR:
        home_endpoint = constants.URL_VISITOR_HOME
    elif role == constants.USER_ROLE_HELPER:
        home_endpoint = constants.URL_HELPER_HOME
    elif role == constants.USER_ROLE_ADMIN:
        home_endpoint = constants.URL_ADMIN_HOME
    else:
        home_endpoint = constants.URL_LOGIN

    return url_for(home_endpoint)

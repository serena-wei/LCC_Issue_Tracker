"""Shared form/input validation helpers."""
import re

from app import constants


def validate_password(password, confirm_password):
    """
    Validates password strength and that it matches the confirmation.

    Returns:
        str | None: An error message if validation fails, or None if valid.
    """
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."
    if password != confirm_password:
        return "The two entered passwords do not match."
    return None


def validate_profile_details(email, password, confirm_password, first_name, last_name, location):
    """
    Validates user profile details.

    Returns:
        tuple: (email_error, password_error, first_name_error, last_name_error, location_error)
               Each value is an error message or None.
    """
    email_error = None
    password_error = None
    first_name_error = None
    last_name_error = None
    location_error = None

    if len(email) > 320:
        email_error = 'Your email address cannot exceed 320 characters.'
    elif not re.match(constants.EMAIL_REGEX, email):
        email_error = 'Invalid email address.'

    if password and confirm_password:
        password_error = validate_password(password, confirm_password)

    if len(first_name) > 50:
        first_name_error = 'Your first name cannot exceed 50 characters.'
    if len(last_name) > 50:
        last_name_error = 'Your last name cannot exceed 50 characters.'
    if len(location) > 50:
        location_error = 'Your location cannot exceed 50 characters.'

    return email_error, password_error, first_name_error, last_name_error, location_error

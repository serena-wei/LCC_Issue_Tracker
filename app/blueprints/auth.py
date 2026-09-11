"""Auth blueprint: login, signup, logout, password reset, root redirect."""
import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import constants
from app.decorators import if_logged_in_redirect
from app.extensions import bcrypt
from app.repositories import users as users_repo
from app.utils import user_home_url
from app.validators import validate_password, validate_profile_details

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def root():
    """Redirects guests to login and logged-in users to their role homepage."""
    return redirect(user_home_url())


@auth_bp.route('/login', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@if_logged_in_redirect
def login():
    """
    Handles user login.

    - GET: Renders the login page.
    - POST: Authenticates the user; redirects to homepage on success,
      or re-renders login with errors on failure.
    """
    if request.method == constants.HTTP_METHOD_POST and constants.USERNAME in request.form and constants.PASSWORD in request.form:
        username = request.form[constants.USERNAME]
        password = request.form[constants.PASSWORD]
        if not username or not password:
            flash("Please enter both username and password.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_LOGIN)

        try:
            account = users_repo.find_by_username(username)
            if account is not None:
                # Inactive users cannot log in
                if account[constants.USER_STATUS] == constants.USER_STATUS_INACTIVE:
                    flash("User is inactive", constants.FLASH_MESSAGE_DANGER)
                    return render_template(constants.TEMPLATE_LOGIN, username=username)
                password_hash = account[constants.PASSWORD_HASH]
                if bcrypt.check_password_hash(password_hash, password):
                    session[constants.SESSION_LOGGED_IN] = True
                    session[constants.USER_ID] = account[constants.USER_ID]
                    session[constants.USERNAME] = account[constants.USERNAME]
                    session[constants.USER_ROLE] = account[constants.USER_ROLE]
                    return redirect(user_home_url())
                return render_template(constants.TEMPLATE_LOGIN,
                                       username=username,
                                       password_invalid=True)
            flash("No matching username found.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_LOGIN)
        except Exception:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_LOGIN), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_LOGIN)


@auth_bp.route('/signup', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@if_logged_in_redirect
def signup():
    """
    Handles user signup.

    - GET: Renders the signup page.
    - POST: Validates form data and creates a new account if valid.
    """
    if (request.method == constants.HTTP_METHOD_POST
            and constants.USERNAME in request.form
            and constants.EMAIL in request.form
            and constants.PASSWORD in request.form
            and constants.CONFIRM_PASSWORD in request.form
            and constants.LOCATION in request.form
            and constants.FIRST_NAME in request.form
            and constants.LAST_NAME in request.form):
        username = request.form[constants.USERNAME]
        email = request.form[constants.EMAIL]
        password = request.form[constants.PASSWORD]
        confirm_password = request.form[constants.CONFIRM_PASSWORD]
        first_name = request.form[constants.FIRST_NAME]
        last_name = request.form[constants.LAST_NAME]
        location = request.form[constants.LOCATION]
        if not password or not confirm_password or not email or not first_name or not last_name or not location or not username:
            flash("Required fields are missing.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_SIGNUP,
                                   username=username,
                                   email=email,
                                   password=password,
                                   confirm_password=confirm_password,
                                   first_name=first_name,
                                   last_name=last_name,
                                   location=location), constants.HTTP_STATUS_CODE_400

        username_error = None
        try:
            account_already_exists = users_repo.username_exists(username)
        except Exception:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_SIGNUP,
                                   username=username,
                                   email=email,
                                   password=password,
                                   confirm_password=confirm_password,
                                   first_name=first_name,
                                   last_name=last_name,
                                   location=location), constants.HTTP_STATUS_CODE_500

        if account_already_exists:
            username_error = 'An account already exists with this username.'
        elif len(username) > 20:
            username_error = 'Your username cannot exceed 20 characters.'
        elif not re.match(constants.USERNAME_PATTERN, username):
            username_error = 'Your username can only contain letters and numbers.'
        email_error, password_error, first_name_error, last_name_error, location_error = validate_profile_details(
            email, password, confirm_password, first_name, last_name, location)
        if (username_error or email_error or password_error or first_name_error or last_name_error or location_error):
            return render_template(constants.TEMPLATE_SIGNUP, username=username, email=email, first_name=first_name,
                                   last_name=last_name, location=location, username_error=username_error,
                                   email_error=email_error, password_error=password_error,
                                   first_name_error=first_name_error,
                                   last_name_error=last_name_error, location_error=location_error)

        password_hash = bcrypt.generate_password_hash(password)
        try:
            users_repo.create_user(username, password_hash, email, first_name, last_name, location)
        except Exception:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_SIGNUP,
                                   username=username,
                                   email=email,
                                   password=password,
                                   confirm_password=confirm_password,
                                   first_name=first_name,
                                   last_name=last_name,
                                   location=location), constants.HTTP_STATUS_CODE_500

        return render_template(constants.TEMPLATE_SIGNUP, signup_successful=True)

    return render_template(constants.TEMPLATE_SIGNUP)


@auth_bp.route('/resetpassword', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
def resetpassword():
    """
    Handles password reset.

    - GET: Renders the reset password page.
    - POST: Validates and updates the password if valid.
    """
    if (request.method == constants.HTTP_METHOD_POST
            and constants.PASSWORD in request.form
            and constants.CONFIRM_PASSWORD in request.form
            and constants.USERNAME in request.form):
        password = request.form[constants.PASSWORD]
        confirm_password = request.form[constants.CONFIRM_PASSWORD]
        username = request.form[constants.USERNAME]
        if not password or not confirm_password or not username:
            flash("Required fields are missing.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_RESETPASSWORD, username=username), constants.HTTP_STATUS_CODE_400

        try:
            user = users_repo.find_auth_by_username(username)
            if not user:
                flash("User does not exist.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_RESETPASSWORD, username=username), constants.HTTP_STATUS_CODE_400

            password_error = validate_password(password, confirm_password)
            if not password_error:
                old_hashed_password = user[constants.PASSWORD_HASH]
                if bcrypt.check_password_hash(old_hashed_password, password):
                    flash("The new password cannot be the same as the original password.", constants.FLASH_MESSAGE_DANGER)
                    return render_template(constants.TEMPLATE_RESETPASSWORD,
                                           username=username), constants.HTTP_STATUS_CODE_400
            if password_error:
                return render_template(constants.TEMPLATE_RESETPASSWORD,
                                       username=username,
                                       password_error=password_error)

            users_repo.update_password_hash(
                user[constants.USER_ID],
                bcrypt.generate_password_hash(password))
            return render_template(constants.TEMPLATE_RESETPASSWORD, reset_password_successful=True)
        except Exception:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_RESETPASSWORD, username=username), constants.HTTP_STATUS_CODE_500
    return render_template(constants.TEMPLATE_RESETPASSWORD)


@auth_bp.route('/logout')
def logout():
    """Clears the session and redirects to the login page."""
    session.pop(constants.SESSION_LOGGED_IN, None)
    session.pop(constants.USER_ID, None)
    session.pop(constants.USERNAME, None)
    session.pop(constants.USER_ROLE, None)

    return redirect(url_for(constants.URL_LOGIN))

"""
The module handles user-related operations, including accessing the homepage of the current role, login, logout, r
egistration, password modification, viewing the user list, bulk modifying user statuses, and modifying user roles.
"""
from app import app, db, constants
from flask import redirect, render_template, request, session, url_for, jsonify, flash
from flask_bcrypt import Bcrypt
import re
# Importing decorators from the current package
from .decorators import login_and_role_required, if_logged_in_redirect

# Create an instance of the Bcrypt class, which we'll be using to hash user
# passwords during login and registration.
flask_bcrypt = Bcrypt(app)

def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user.
    
    If the user is not logged in, or the role stored in their session cookie is
    invalid, this returns the URL for the login page instead."""
    role = session.get(constants.USER_ROLE, None)

    if role==constants.USER_ROLE_VISITOR:
        home_endpoint = constants.URL_VISITOR_HOME
    elif role==constants.USER_ROLE_HELPER:
        home_endpoint=constants.URL_HELPER_HOME
    elif role==constants.USER_ROLE_ADMIN:
        home_endpoint=constants.URL_ADMIN_HOME
    else:
        home_endpoint = constants.URL_LOGIN
    
    return url_for(home_endpoint)

@app.route('/')
def root():
    """Root endpoint (/)
    
    Methods:
    - get: Redirects guests to the login page, and redirects logged-in users to
        their own role-specific homepage.
    """
    return redirect(user_home_url())

@app.route('/login', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@if_logged_in_redirect
def login():
    """Handles user login.
    
    This endpoint supports both GET and POST requests:
    
    - GET: Renders the login page.
    - POST: Attempts to authenticate the user using the provided username and password.
      - If authentication is successful, redirects the user to their role-specific homepage.
      - If authentication fails, re-renders the login page with appropriate error messages.

    If a user is already logged in, they are redirected to their homepage instead of seeing the login form.
    
    Returns:
        - A rendered login page (for GET requests or failed login attempts).
        - A redirection to the user's homepage upon successful login.
    """
    # Check if this is a POST request and the username & password fields exist in the request form.
    if request.method==constants.HTTP_METHOD_POST and constants.USERNAME in request.form and constants.PASSWORD in request.form:
        # Get the login details submitted by the user.
        username = request.form[constants.USERNAME]
        password = request.form[constants.PASSWORD]
        if not username or not password:
            flash("Please enter both username and password.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_LOGIN)

        try:
            # Attempt to validate the login details against the database.
            with db.get_cursor() as cursor:
                cursor.execute('''
                            SELECT user_id, username, password_hash, role, status
                            FROM users
                            WHERE username = %s;
                            ''', (username,))
                account = cursor.fetchone()
                if account is not None:
                    # 未激活用户不可登录
                    if account[constants.USER_STATUS]==constants.USER_STATUS_INACTIVE:
                        # No matching username found in the database.
                        flash("User is inactive", constants.FLASH_MESSAGE_DANGER)
                        return render_template(constants.TEMPLATE_LOGIN,username=username)
                    # Retrieve stored password hash from the database.
                    password_hash = account[constants.PASSWORD_HASH]
                    # Verify the provided password against the stored hash.
                    if flask_bcrypt.check_password_hash(password_hash, password):
                        # Authentication successful: store user session data.
                        session[constants.SESSION_LOGGED_IN] = True
                        session[constants.USER_ID] = account[constants.USER_ID]
                        session[constants.USERNAME] = account[constants.USERNAME]
                        session[constants.USER_ROLE] = account[constants.USER_ROLE]

                        return redirect(user_home_url())
                    else:
                        # Password is incorrect. Re-display the login form, keeping
                        # the username provided by the user so they don't need to
                        # re-enter it. We also set a `password_invalid` flag that
                        # the template uses to display a validation message.
                        return render_template(constants.TEMPLATE_LOGIN,
                                            username=username,
                                            password_invalid=True)
                else:
                    # No matching username found in the database.
                    flash("No matching username found.", constants.FLASH_MESSAGE_DANGER)
                    return render_template(constants.TEMPLATE_LOGIN)
        except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_LOGIN), constants.HTTP_STATUS_CODE_500

    # This was a GET request, or an invalid POST (no username and/or password),
    # so we just render the login form with no pre-populated details or flags.
    return render_template(constants.TEMPLATE_LOGIN)

@app.route('/signup', methods=[constants.HTTP_METHOD_GET,constants.HTTP_METHOD_POST])
@if_logged_in_redirect
def signup():
    """
    Handles user signup.
    
    - GET request: Renders the signup page.
    - POST request: Validates the submitted form, checks for existing users, and creates a new account if valid.
    
    Returns:
        - If the user is already logged in, redirects to their home page.
        - If there are validation errors, re-renders the signup page with error messages.
        - If registration is successful, shows a success message.
    """
    if request.method == constants.HTTP_METHOD_POST and constants.USERNAME in request.form and constants.EMAIL in request.form and constants.PASSWORD in request.form and constants.CONFIRM_PASSWORD in request.form and constants.LOCATION in request.form and constants.FIRST_NAME in request.form and constants.LAST_NAME in request.form:
        username = request.form[constants.USERNAME]
        email = request.form[constants.EMAIL]
        password = request.form[constants.PASSWORD]
        confirm_password = request.form[constants.CONFIRM_PASSWORD]
        first_name = request.form[constants.FIRST_NAME]
        last_name = request.form[constants.LAST_NAME]
        location = request.form[constants.LOCATION]
        # Check if all required fields exist in the form submission
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
            # Check whether there's an account with this username in the database.
            with db.get_cursor() as cursor:
                cursor.execute('SELECT user_id FROM users WHERE username = %s;',
                            (username,))
                account_already_exists = cursor.fetchone() is not None
        except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_SIGNUP, 
                                   username=username,
                                   email=email,
                                   password=password,
                                   confirm_password=confirm_password,
                                   first_name=first_name,
                                   last_name=last_name,
                                   location=location), constants.HTTP_STATUS_CODE_500
        
        # Validate the username, ensuring that it's unique (as we just checked
        # above) and meets the naming constraints of our web app.
        if account_already_exists:
            username_error = 'An account already exists with this username.'
        elif len(username) > 20:
            username_error = 'Your username cannot exceed 20 characters.'
        elif not re.match(constants.USERNAME_PATTERN, username):
            username_error = 'Your username can only contain letters and numbers.'   
        # Validate other profile details         
        email_error, password_error, first_name_error, last_name_error, location_error = validate_profile_details(email, password, confirm_password, first_name, last_name, location)
        # If there are any validation errors, re-render the signup page with messages
        if (username_error or email_error or password_error or first_name_error or last_name_error or location_error):
            return render_template(constants.TEMPLATE_SIGNUP,username=username,email=email,first_name=first_name,
                                   last_name=last_name,location=location,username_error=username_error,
                                   email_error=email_error,password_error=password_error,first_name_error = first_name_error,
                                   last_name_error = last_name_error,location_error = location_error)
        else:
            # Hash the password for security
            password_hash = flask_bcrypt.generate_password_hash(password)
            try:
                with db.get_cursor() as cursor:
                    cursor.execute('''
                                INSERT INTO users (username, password_hash, email, first_name, last_name, location, role, profile_image, status)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                                ''',
                                (username, password_hash, email, first_name, last_name, location, constants.USER_ROLE_VISITOR, constants.STATIC_IMAGES_URL+constants.DEFAULT_PROFILE_IMAGE_NAME, constants.USER_STATUS_ACTIVE))
            except Exception as e:
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

def validate_profile_details(email, password, confirm_password, first_name, last_name, location):
    """
    Validates user profile details.

    Args:
        email (str): The user's email address.
        password (str): The user's password (optional for profile updates).
        confirm_password (str): Confirmation of the password (optional for profile updates).
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        location (str): The user's location.

    Returns:
        tuple: (email_error, password_error, first_name_error, last_name_error, location_error)
               Each value is either an error message (if validation fails) or None (if validation passes).
    """
    # We start by assuming that everything is okay. If we encounter any
    # errors during validation, we'll store an error message in one or more
    # of these variables so we can pass them through to the template.
    email_error = None
    password_error = None
    first_name_error = None
    last_name_error = None
    location_error = None

    # Validate the new user's email address. 
    if len(email) > 320:
        email_error = 'Your email address cannot exceed 320 characters.'
    elif not re.match(constants.EMAIL_REGEX, email):
        email_error = 'Invalid email address.'
            
    # Validate password.
    # Validate the password based on length, case, number, and special character requirements, 
    # and ensure that both password entries match.
    if password and confirm_password:
        password_error = validate_password(password, confirm_password)

    # Validate the new user's firstname, lastname and location. 
    if len(first_name) > 50:
        first_name_error = 'Your first name cannot exceed 50 characters.'
    if len(last_name) > 50:
        last_name_error = 'Your last name cannot exceed 50 characters.'
    if len(location) > 50:
        location_error = 'Your location cannot exceed 50 characters.'
    
    return email_error, password_error, first_name_error, last_name_error, location_error

def validate_password(password, confirm_password):
    """
    Validates the strength and correctness of a password.

    This function checks whether the provided password meets security requirements, 
    including length, uppercase and lowercase letters, numbers, and special characters. 
    It also verifies that the password matches the confirmation input.

    Args:
        password (str): The user's chosen password.
        confirm_password (str): The password confirmation input by the user.

    Returns:
        str | None: An error message if validation fails, or None if the password is valid.
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
    
@app.route('/resetpassword', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
def resetpassword():
    """
    Handles the password reset process.

    - GET request: Renders the password reset page.
    - POST request: Validates the submitted form, checks if the user exists, verifies the password, and updates it if valid.

    Returns:
        - If there are validation errors, re-renders the reset password page with error messages.
        - If the password is successfully reset, shows a success message.
        - If there is an error during processing, returns a server error page.
    """
    if request.method==constants.HTTP_METHOD_POST and constants.PASSWORD in request.form and constants.CONFIRM_PASSWORD in request.form and constants.USERNAME in request.form:
        password = request.form[constants.PASSWORD]
        confirm_password = request.form[constants.CONFIRM_PASSWORD]
        username = request.form[constants.USERNAME]
        # Check if any of the required fields are missing
        if not password or not confirm_password or not username:
            flash("Required fields are missing.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_RESETPASSWORD, username = username), constants.HTTP_STATUS_CODE_400

        try:
            # Check whether there's an account with this username in the database.
            with db.get_cursor() as cursor:
                cursor.execute('SELECT user_id, password_hash FROM users WHERE username = %s;',
                            (username,))
                user = cursor.fetchone()
            # If no user found, display an error message
            if not user:
                user=None
                flash("User does not exist.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_RESETPASSWORD, username = username), constants.HTTP_STATUS_CODE_400
            else:
                # Validate password and confirm password
                password_error = validate_password(password, confirm_password)
                if not password_error:
                    # If password is valid, check if the new password is the same as the old one
                    old_hashed_password = user[constants.PASSWORD_HASH]
                    if flask_bcrypt.check_password_hash(old_hashed_password, password):
                        flash("The new password cannot be the same as the original password.", constants.FLASH_MESSAGE_DANGER)
                        return render_template(constants.TEMPLATE_RESETPASSWORD,
                                    username = username), constants.HTTP_STATUS_CODE_400
            if (password_error):
                return render_template(constants.TEMPLATE_RESETPASSWORD, 
                                username = username, 
                                password_error = password_error
                                )
            else:
                # If no validation errors, hash the new password and update it in the database
                with db.get_cursor() as cursor:
                    cursor.execute('UPDATE users SET password_hash=%s WHERE user_id = %s;',
                        (flask_bcrypt.generate_password_hash(password), user[constants.USER_ID]))
                return render_template(constants.TEMPLATE_RESETPASSWORD, reset_password_successful=True)
        except Exception as e:
            # Handle any exceptions that occur during the process
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_RESETPASSWORD, username = username), constants.HTTP_STATUS_CODE_500
    # If it's a GET request, or the POST request is missing required fields, render the reset password page
    return render_template(constants.TEMPLATE_RESETPASSWORD)

@app.route('/userlist')
@login_and_role_required([constants.USER_ROLE_ADMIN])
def user_list():
    """
    This method displays the user list page, which is accessible only by admins.

    - If the user is not logged in, they are redirected to the login page.
    - If the user is not an admin, an "Access Denied" page is returned.
    - If a database query fails, a 500 error page is returned.
    - If the user data is successfully queried, the user list page is returned.

    Returns:
        - Renders the user list page and passes the queried user data.
    """
    try:
        # Use the database cursor to query all user information, ordered by status
        with db.get_cursor() as cursor:
            cursor.execute('SELECT * FROM users ORDER BY status;')
            users = cursor.fetchall()
    except Exception as e:
        flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_USER_LIST, users=[]), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_USER_LIST, users=users)

@app.route('/user/changeBatchStatus', methods=[constants.HTTP_METHOD_POST])
@login_and_role_required([constants.USER_ROLE_ADMIN])
def change_user_status():
    """
    This function handles the request to update the status of multiple users in batch.
    It checks if the user is logged in and has admin privileges, then updates the status
    of selected users based on the provided user IDs and status.

    Returns:
        JSON response with a message indicating success or error.
    """
    # Get JSON data from the POST request
    data = request.get_json()
    user_ids = data.get(constants.USER_IDS_KEY)
    status = data.get(constants.USER_STATUS)
    if user_ids:
        # Convert the list of user IDs into a format suitable for the query
        user_ids_list = user_ids
        # Prepare a placeholder string for the number of user IDs
        placeholders = ', '.join(['%s'] * len(user_ids_list))

        # Execute the update query
        try:
            with db.get_cursor() as cursor:
                cursor.execute(f'UPDATE users SET status = %s WHERE user_id IN ({placeholders});', [status] + user_ids_list)
        except Exception as e:
            return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500
    else:
        # If no user_ids provided, return an error response
        return jsonify({"error": "No user IDs provided. Please select at least one user to update status."}), constants.HTTP_STATUS_CODE_400

    return jsonify({"message": "Status updated successfully."})


@app.route('/user/changeRole', methods=[constants.HTTP_METHOD_POST])
@login_and_role_required([constants.USER_ROLE_ADMIN])
def change_user_role():
    """
    Change the role of a user. Only accessible by administrators.

    HTTP Method: POST
    Endpoint: /user/changeRole

    Request Body (JSON):
    {
        "user_id": <int>,  # The ID of the user whose role is to be changed
        "role": <string>    # The new role to be assigned
    }

    Responses:
        JSON response with a message indicating success or error.
    """
    # Get JSON data from the POST request
    data = request.get_json()
    user_id = data.get(constants.USER_ID)
    role = data.get(constants.USER_ROLE)
    if user_id and role:
        try:
            # Update the user's role in the database
            with db.get_cursor() as cursor:
                cursor.execute('UPDATE users SET role = %s WHERE user_id = %s;', [role, user_id])
        except Exception as e:
            return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500
    else:
        return jsonify({"error": "Invalid data provided. User ID and role are required."}), constants.HTTP_STATUS_CODE_400

    return jsonify({"message": "Role updated successfully."})
    
@app.route('/logout')
def logout():
    """Logout endpoint.

    Methods:
    - get: Logs the current user out (if they were logged in to begin with),
        and redirects them to the login page.
    """
    # Rremove the cookie from their web browser.
    session.pop(constants.SESSION_LOGGED_IN, None)
    session.pop(constants.USER_ID, None)
    session.pop(constants.USERNAME, None)
    session.pop(constants.USER_ROLE, None)
    
    return redirect(url_for('login'))
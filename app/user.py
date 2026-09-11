"""
User operations: login, logout, registration, password reset,
user list, batch status updates, and role changes.
"""
from app import app, db, constants
from flask import redirect, render_template, request, session, url_for, jsonify, flash
from flask_bcrypt import Bcrypt
import re
from .decorators import login_and_role_required, if_logged_in_redirect

flask_bcrypt = Bcrypt(app)

def user_home_url():
    """Returns the homepage URL for the current user, or the login URL if not logged in."""
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
    """Redirects guests to login and logged-in users to their role homepage."""
    return redirect(user_home_url())

@app.route('/login', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@if_logged_in_redirect
def login():
    """
    Handles user login.

    - GET: Renders the login page.
    - POST: Authenticates the user; redirects to homepage on success,
      or re-renders login with errors on failure.
    """
    if request.method==constants.HTTP_METHOD_POST and constants.USERNAME in request.form and constants.PASSWORD in request.form:
        username = request.form[constants.USERNAME]
        password = request.form[constants.PASSWORD]
        if not username or not password:
            flash("Please enter both username and password.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_LOGIN)

        try:
            with db.get_cursor() as cursor:
                cursor.execute('''
                            SELECT user_id, username, password_hash, role, status
                            FROM users
                            WHERE username = %s;
                            ''', (username,))
                account = cursor.fetchone()
                if account is not None:
                    # Inactive users cannot log in
                    if account[constants.USER_STATUS]==constants.USER_STATUS_INACTIVE:
                        flash("User is inactive", constants.FLASH_MESSAGE_DANGER)
                        return render_template(constants.TEMPLATE_LOGIN,username=username)
                    password_hash = account[constants.PASSWORD_HASH]
                    if flask_bcrypt.check_password_hash(password_hash, password):
                        session[constants.SESSION_LOGGED_IN] = True
                        session[constants.USER_ID] = account[constants.USER_ID]
                        session[constants.USERNAME] = account[constants.USERNAME]
                        session[constants.USER_ROLE] = account[constants.USER_ROLE]

                        return redirect(user_home_url())
                    else:
                        return render_template(constants.TEMPLATE_LOGIN,
                                            username=username,
                                            password_invalid=True)
                else:
                    flash("No matching username found.", constants.FLASH_MESSAGE_DANGER)
                    return render_template(constants.TEMPLATE_LOGIN)
        except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_LOGIN), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_LOGIN)

@app.route('/signup', methods=[constants.HTTP_METHOD_GET,constants.HTTP_METHOD_POST])
@if_logged_in_redirect
def signup():
    """
    Handles user signup.

    - GET: Renders the signup page.
    - POST: Validates form data and creates a new account if valid.
    """
    if request.method == constants.HTTP_METHOD_POST and constants.USERNAME in request.form and constants.EMAIL in request.form and constants.PASSWORD in request.form and constants.CONFIRM_PASSWORD in request.form and constants.LOCATION in request.form and constants.FIRST_NAME in request.form and constants.LAST_NAME in request.form:
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
        
        if account_already_exists:
            username_error = 'An account already exists with this username.'
        elif len(username) > 20:
            username_error = 'Your username cannot exceed 20 characters.'
        elif not re.match(constants.USERNAME_PATTERN, username):
            username_error = 'Your username can only contain letters and numbers.'   
        email_error, password_error, first_name_error, last_name_error, location_error = validate_profile_details(email, password, confirm_password, first_name, last_name, location)
        if (username_error or email_error or password_error or first_name_error or last_name_error or location_error):
            return render_template(constants.TEMPLATE_SIGNUP,username=username,email=email,first_name=first_name,
                                   last_name=last_name,location=location,username_error=username_error,
                                   email_error=email_error,password_error=password_error,first_name_error = first_name_error,
                                   last_name_error = last_name_error,location_error = location_error)
        else:
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
    
@app.route('/resetpassword', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
def resetpassword():
    """
    Handles password reset.

    - GET: Renders the reset password page.
    - POST: Validates and updates the password if valid.
    """
    if request.method==constants.HTTP_METHOD_POST and constants.PASSWORD in request.form and constants.CONFIRM_PASSWORD in request.form and constants.USERNAME in request.form:
        password = request.form[constants.PASSWORD]
        confirm_password = request.form[constants.CONFIRM_PASSWORD]
        username = request.form[constants.USERNAME]
        if not password or not confirm_password or not username:
            flash("Required fields are missing.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_RESETPASSWORD, username = username), constants.HTTP_STATUS_CODE_400

        try:
            with db.get_cursor() as cursor:
                cursor.execute('SELECT user_id, password_hash FROM users WHERE username = %s;',
                            (username,))
                user = cursor.fetchone()
            if not user:
                user=None
                flash("User does not exist.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_RESETPASSWORD, username = username), constants.HTTP_STATUS_CODE_400
            else:
                password_error = validate_password(password, confirm_password)
                if not password_error:
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
                with db.get_cursor() as cursor:
                    cursor.execute('UPDATE users SET password_hash=%s WHERE user_id = %s;',
                        (flask_bcrypt.generate_password_hash(password), user[constants.USER_ID]))
                return render_template(constants.TEMPLATE_RESETPASSWORD, reset_password_successful=True)
        except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_RESETPASSWORD, username = username), constants.HTTP_STATUS_CODE_500
    return render_template(constants.TEMPLATE_RESETPASSWORD)

@app.route('/userlist')
@login_and_role_required([constants.USER_ROLE_ADMIN])
def user_list():
    """Displays the user list page (admin only)."""
    try:
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
    """Batch-updates status for selected users (admin only)."""
    data = request.get_json()
    user_ids = data.get(constants.USER_IDS_KEY)
    status = data.get(constants.USER_STATUS)
    if user_ids:
        user_ids_list = user_ids
        placeholders = ', '.join(['%s'] * len(user_ids_list))

        try:
            with db.get_cursor() as cursor:
                cursor.execute(f'UPDATE users SET status = %s WHERE user_id IN ({placeholders});', [status] + user_ids_list)
        except Exception as e:
            return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500
    else:
        return jsonify({"error": "No user IDs provided. Please select at least one user to update status."}), constants.HTTP_STATUS_CODE_400

    return jsonify({"message": "Status updated successfully."})


@app.route('/user/changeRole', methods=[constants.HTTP_METHOD_POST])
@login_and_role_required([constants.USER_ROLE_ADMIN])
def change_user_role():
    """Changes a user's role (admin only)."""
    data = request.get_json()
    user_id = data.get(constants.USER_ID)
    role = data.get(constants.USER_ROLE)
    if user_id and role:
        try:
            with db.get_cursor() as cursor:
                cursor.execute('UPDATE users SET role = %s WHERE user_id = %s;', [role, user_id])
        except Exception as e:
            return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500
    else:
        return jsonify({"error": "Invalid data provided. User ID and role are required."}), constants.HTTP_STATUS_CODE_400

    return jsonify({"message": "Role updated successfully."})
    
@app.route('/logout')
def logout():
    """Clears the session and redirects to the login page."""
    session.pop(constants.SESSION_LOGGED_IN, None)
    session.pop(constants.USER_ID, None)
    session.pop(constants.USERNAME, None)
    session.pop(constants.USER_ROLE, None)
    
    return redirect(url_for('login'))

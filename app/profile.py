"""
This module handles the user profile page, including viewing and editing profile information.
"""
from app import app, db, user, constants
from flask import redirect, render_template, request, session, url_for, flash
# Importing decorators from the current package
from .decorators import login_required
import os
    
@app.route('/profile')
@login_required
def profile():
    """
    Handles the user profile page.

    This function retrieves the logged-in user's profile information from the database
    and renders the profile page. If the user is not logged in, they are redirected to 
    the login page. If the profile is not found, a flash message is displayed.

    Returns:
        - If the user is not logged in: Redirects to the login page.
        - If the profile is found: Renders the profile page (view or edit mode).
        - If an error occurs: Displays an error message and returns a 500 status code.
    """
    profile=None
    try:
        # Retrieve user profile from the database.
        with db.get_cursor() as cursor:
            cursor.execute('SELECT username, email, role, first_name, last_name, location, profile_image FROM users WHERE user_id = %s;',
                        (session[constants.USER_ID],))
            profile = cursor.fetchone()
            if profile is None:
                flash("User profile not found.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_PROFILE, profile=profile), constants.HTTP_STATUS_CODE_404
    except Exception as e:
        flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_PROFILE, profile=profile), constants.HTTP_STATUS_CODE_500

    # Get the 'mode' parameter from the URL (default to an empty string if not provided)
    # Distinguish between viewing and editing operations
    mode = request.args.get(constants.URL_PARAMETER_MODE, '')
    return render_template(constants.TEMPLATE_PROFILE, mode=mode, profile=profile)

@app.route('/profile/edit', methods=[constants.HTTP_METHOD_POST])
@login_required
def profile_edit():
    """
    Handles the profile editing functionality for logged-in users.
    This method validates the profile form submitted by the user, including
    the email, first name, last name, location, and profile image. If the 
    form is valid, it updates the user's profile information in the database.

    If an image is uploaded, it saves the image in the appropriate folder 
    and updates the profile image field in the database. If the user chooses 
    to delete the image, it resets the profile image to the default.

    Args:
        None

    Returns:
        - Redirects to the user's profile page on successful update.
        - Renders the profile page with appropriate error messages in case 
          of validation failure or exception during the update process.
        - Redirects to the login page if the session is not logged in.
    """
    if constants.EMAIL in request.form and constants.LOCATION in request.form and constants.FIRST_NAME in request.form and constants.LAST_NAME in request.form and constants.USERNAME in request.form and constants.USER_PROFILE_IMAGE in request.form:
        email = request.form[constants.EMAIL]
        first_name = request.form[constants.FIRST_NAME]
        last_name = request.form[constants.LAST_NAME]
        location = request.form[constants.LOCATION]
        username = request.form[constants.USERNAME]
        profile_image = request.form[constants.USER_PROFILE_IMAGE]
        delete_image = request.form.get(constants.DELETE_IMAGE, constants.DELETE_IMAGE_NOT_PERFORMED)
        uploaded_image = request.files.get(constants.USER_PROFILE_IMAGE) 

        if not email or not first_name or not last_name or not location or not username:
            flash("Required fields are missing.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_PROFILE, mode = constants.URL_PARAMETER_MODE_EDIT), constants.HTTP_STATUS_CODE_400

        role = session.get(constants.USER_ROLE)
        if not role:
            flash("User role is missing. Please log out and log in again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_PROFILE, 
                                   mode = constants.URL_PARAMETER_MODE_EDIT,
                                   profile = profile), constants.HTTP_STATUS_CODE_400

        # Validates the profile details
        email_error, password_error, first_name_error, last_name_error, location_error = user.validate_profile_details(email, '', '', first_name, last_name, location)
    
        profile = {
            constants.USERNAME: username,
            constants.EMAIL: email,
            constants.FIRST_NAME: first_name,
            constants.LAST_NAME: last_name,
            constants.LOCATION: location,
            constants.USER_ROLE: role
        }
        if (email_error or first_name_error or last_name_error or location_error):
                # One or more errors were encountered, so send the user back to the profile page 
                return render_template(constants.TEMPLATE_PROFILE,
                                    mode = constants.URL_PARAMETER_MODE_EDIT,
                                    profile=profile,
                                    email_error=email_error,
                                    first_name_error = first_name_error,
                                    last_name_error = last_name_error,
                                    location_error = location_error
                                    )
        else:
            if uploaded_image:  # If the user uploaded a new image
                # Get the file extension of the uploaded file
                file_extension = os.path.splitext(uploaded_image.filename)[1]
                # Set the folder path
                folder_path = os.path.join(os.path.dirname(__file__), constants.STATIC_IMAGES_PATH)
                # Ensure the folder exists, create it if it doesn't
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                # Set the filename to 'profile_image' and retain the file extension
                filename = constants.USER_PROFILE_IMAGE + '_' + session[constants.USERNAME]+ file_extension
                if not allowed_file(filename):
                    flash("The uploaded profile image type is not jpg, jpeg, or png.", constants.FLASH_MESSAGE_DANGER)
                    return render_template(constants.TEMPLATE_PROFILE, 
                                           mode = constants.URL_PARAMETER_MODE_EDIT,
                                           profile = profile), constants.HTTP_STATUS_CODE_400
                # Set the full file path to save the image
                filepath = os.path.join(folder_path, filename)
                # Save the file
                uploaded_image.save(filepath)
                # Store the saved file path in the database (relative path)
                new_profile_image = os.path.join(constants.STATIC_IMAGES_URL, filename)
            elif delete_image == constants.DELETE_IMAGE_PERFORMED:  # If the user chose to delete the image
                new_profile_image = constants.STATIC_IMAGES_URL + constants.DEFAULT_PROFILE_IMAGE_NAME  # Set the profile image to default, indicating deletion
            else:
                # If no changes were made to the profile image, keep the original image
                new_profile_image = profile_image
            try:
                with db.get_cursor() as cursor:
                    cursor.execute('UPDATE users SET email=%s, first_name=%s, last_name=%s, location=%s, profile_image=%s WHERE user_id = %s;',
                        (request.form[constants.EMAIL], request.form[constants.FIRST_NAME], request.form[constants.LAST_NAME], request.form[constants.LOCATION], new_profile_image, session[constants.USER_ID]))
                return redirect(url_for(constants.USER_ROLE_PROFILE))
            except Exception as e:
                flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_PROFILE, profile=profile), constants.HTTP_STATUS_CODE_500
            
    return render_template(constants.TEMPLATE_LOGIN)

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed image extension (jpg, jpeg, png).

    Args:
        filename (str): The name of the file being uploaded.

    Returns:
        bool: True if the file extension is valid, False otherwise.
    """
    # Get the file extension and convert it to lowercase.
    ext = os.path.splitext(filename)[1].lower()[1:]
    return ext in constants.ALLOWED_IMAGE_EXTENSIONS

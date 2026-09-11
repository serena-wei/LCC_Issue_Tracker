"""Users blueprint: profile, admin user management, role home pages."""
import os

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, session, url_for

from app import constants, db
from app.decorators import login_and_role_required, login_required, role_required
from app.validators import validate_profile_details

users_bp = Blueprint('users', __name__)


@users_bp.route('/visitor/home')
@role_required(constants.USER_ROLE_VISITOR)
def visitor_home():
    """Renders the visitor homepage."""
    return render_template(constants.TEMPLATE_VISITOR_HOME)


@users_bp.route('/helper/home')
@role_required(constants.USER_ROLE_HELPER)
def helper_home():
    """Renders the helper homepage."""
    return render_template(constants.TEMPLATE_HELPER_HOME)


@users_bp.route('/admin/home')
@role_required(constants.USER_ROLE_ADMIN)
def admin_home():
    """Renders the admin homepage."""
    return render_template(constants.TEMPLATE_ADMIN_HOME)


@users_bp.route('/userlist')
@login_and_role_required([constants.USER_ROLE_ADMIN])
def user_list():
    """Displays the user list page (admin only)."""
    try:
        with db.get_cursor() as cursor:
            cursor.execute('SELECT * FROM users ORDER BY status;')
            users = cursor.fetchall()
    except Exception:
        flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_USER_LIST, users=[]), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_USER_LIST, users=users)


@users_bp.route('/user/changeBatchStatus', methods=[constants.HTTP_METHOD_POST])
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
                cursor.execute(
                    f'UPDATE users SET status = %s WHERE user_id IN ({placeholders});',
                    [status] + user_ids_list)
        except Exception:
            return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500
    else:
        return jsonify({"error": "No user IDs provided. Please select at least one user to update status."}), constants.HTTP_STATUS_CODE_400

    return jsonify({"message": "Status updated successfully."})


@users_bp.route('/user/changeRole', methods=[constants.HTTP_METHOD_POST])
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
        except Exception:
            return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500
    else:
        return jsonify({"error": "Invalid data provided. User ID and role are required."}), constants.HTTP_STATUS_CODE_400

    return jsonify({"message": "Role updated successfully."})


@users_bp.route('/profile')
@login_required
def profile():
    """
    Displays the logged-in user's profile.

    Supports view and edit modes via the `mode` URL parameter.
    """
    profile = None
    try:
        with db.get_cursor() as cursor:
            cursor.execute(
                'SELECT username, email, role, first_name, last_name, location, profile_image FROM users WHERE user_id = %s;',
                (session[constants.USER_ID],))
            profile = cursor.fetchone()
            if profile is None:
                flash("User profile not found.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_PROFILE, profile=profile), constants.HTTP_STATUS_CODE_404
    except Exception:
        flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_PROFILE, profile=profile), constants.HTTP_STATUS_CODE_500

    mode = request.args.get(constants.URL_PARAMETER_MODE, '')
    return render_template(constants.TEMPLATE_PROFILE, mode=mode, profile=profile)


@users_bp.route('/profile/edit', methods=[constants.HTTP_METHOD_POST])
@login_required
def profile_edit():
    """Updates the logged-in user's profile details and optional profile image."""
    if (constants.EMAIL in request.form
            and constants.LOCATION in request.form
            and constants.FIRST_NAME in request.form
            and constants.LAST_NAME in request.form
            and constants.USERNAME in request.form
            and constants.USER_PROFILE_IMAGE in request.form):
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
            return render_template(constants.TEMPLATE_PROFILE, mode=constants.URL_PARAMETER_MODE_EDIT), constants.HTTP_STATUS_CODE_400

        role = session.get(constants.USER_ROLE)
        profile = {
            constants.USERNAME: username,
            constants.EMAIL: email,
            constants.FIRST_NAME: first_name,
            constants.LAST_NAME: last_name,
            constants.LOCATION: location,
            constants.USER_ROLE: role
        }
        if not role:
            flash("User role is missing. Please log out and log in again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_PROFILE,
                                   mode=constants.URL_PARAMETER_MODE_EDIT,
                                   profile=profile), constants.HTTP_STATUS_CODE_400

        email_error, password_error, first_name_error, last_name_error, location_error = validate_profile_details(
            email, '', '', first_name, last_name, location)

        if email_error or first_name_error or last_name_error or location_error:
            return render_template(constants.TEMPLATE_PROFILE,
                                   mode=constants.URL_PARAMETER_MODE_EDIT,
                                   profile=profile,
                                   email_error=email_error,
                                   first_name_error=first_name_error,
                                   last_name_error=last_name_error,
                                   location_error=location_error)
        else:
            if uploaded_image:
                file_extension = os.path.splitext(uploaded_image.filename)[1]
                folder_path = os.path.join(current_app.root_path, constants.STATIC_IMAGES_PATH)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                filename = constants.USER_PROFILE_IMAGE + '_' + session[constants.USERNAME] + file_extension
                if not allowed_file(filename):
                    flash("The uploaded profile image type is not jpg, jpeg, or png.", constants.FLASH_MESSAGE_DANGER)
                    return render_template(constants.TEMPLATE_PROFILE,
                                           mode=constants.URL_PARAMETER_MODE_EDIT,
                                           profile=profile), constants.HTTP_STATUS_CODE_400
                filepath = os.path.join(folder_path, filename)
                uploaded_image.save(filepath)
                new_profile_image = os.path.join(constants.STATIC_IMAGES_URL, filename)
            elif delete_image == constants.DELETE_IMAGE_PERFORMED:
                new_profile_image = constants.STATIC_IMAGES_URL + constants.DEFAULT_PROFILE_IMAGE_NAME
            else:
                new_profile_image = profile_image
            try:
                with db.get_cursor() as cursor:
                    cursor.execute(
                        'UPDATE users SET email=%s, first_name=%s, last_name=%s, location=%s, profile_image=%s WHERE user_id = %s;',
                        (request.form[constants.EMAIL], request.form[constants.FIRST_NAME],
                         request.form[constants.LAST_NAME], request.form[constants.LOCATION],
                         new_profile_image, session[constants.USER_ID]))
                return redirect(url_for(constants.URL_PROFILE))
            except Exception:
                flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_PROFILE, profile=profile), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_LOGIN)


def allowed_file(filename):
    """Returns True if the file has an allowed image extension (jpg, jpeg, png)."""
    ext = os.path.splitext(filename)[1].lower()[1:]
    return ext in constants.ALLOWED_IMAGE_EXTENSIONS

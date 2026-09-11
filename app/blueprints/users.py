"""Users blueprint: profile, admin user management, role home pages."""
import os

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, session, url_for

from app import constants
from app.decorators import login_and_role_required, login_required, role_required
from app.repositories import users as users_repo
from app.validators import validate_profile_details

users_bp = Blueprint('users', __name__)


@users_bp.route('/visitor/home')
@role_required(constants.USER_ROLE_VISITOR)
def visitor_home():
    """Renders the visitor homepage."""
    return render_template('visitor_home.html')


@users_bp.route('/helper/home')
@role_required(constants.USER_ROLE_HELPER)
def helper_home():
    """Renders the helper homepage."""
    return render_template('helper_home.html')


@users_bp.route('/admin/home')
@role_required(constants.USER_ROLE_ADMIN)
def admin_home():
    """Renders the admin homepage."""
    return render_template('admin_home.html')


@users_bp.route('/userlist')
@login_and_role_required([constants.USER_ROLE_ADMIN])
def user_list():
    """Displays the user list page (admin only)."""
    try:
        users = users_repo.list_all_ordered_by_status()
    except Exception:
        flash("An error occurred while processing your request. Please try again.", 'danger')
        return render_template('user_list.html', users=[]), 500

    return render_template('user_list.html', users=users)


@users_bp.route('/user/changeBatchStatus', methods=['POST'])
@login_and_role_required([constants.USER_ROLE_ADMIN])
def change_user_status():
    """Batch-updates status for selected users (admin only)."""
    data = request.get_json()
    user_ids = data.get(constants.USER_IDS)
    status = data.get(constants.USER_STATUS)
    if not user_ids:
        return jsonify({"error": "No user IDs provided. Please select at least one user to update status."}), 400

    try:
        users_repo.update_status_for_ids(user_ids, status)
    except Exception:
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

    return jsonify({"message": "Status updated successfully."})


@users_bp.route('/user/changeRole', methods=['POST'])
@login_and_role_required([constants.USER_ROLE_ADMIN])
def change_user_role():
    """Changes a user's role (admin only)."""
    data = request.get_json()
    user_id = data.get(constants.USER_ID)
    role = data.get(constants.USER_ROLE)
    if not user_id or not role:
        return jsonify({"error": "Invalid data provided. User ID and role are required."}), 400

    try:
        users_repo.update_role(user_id, role)
    except Exception:
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

    return jsonify({"message": "Role updated successfully."})


@users_bp.route('/profile')
@login_required
def profile():
    """
    Displays the logged-in user's profile.

    Supports view and edit modes via the `mode` URL parameter.
    """
    profile_data = None
    try:
        profile_data = users_repo.get_profile(session[constants.USER_ID])
        if profile_data is None:
            flash("User profile not found.", 'danger')
            return render_template('profile.html', profile=profile_data), 404
    except Exception:
        flash("An error occurred while processing your request. Please try again.", 'danger')
        return render_template('profile.html', profile=profile_data), 500

    mode = request.args.get('mode', '')
    return render_template('profile.html', mode=mode, profile=profile_data)


@users_bp.route('/profile/edit', methods=['POST'])
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
            flash("Required fields are missing.", 'danger')
            return render_template('profile.html', mode='edit'), 400

        role = session.get(constants.USER_ROLE)
        profile_data = {
            constants.USERNAME: username,
            constants.EMAIL: email,
            constants.FIRST_NAME: first_name,
            constants.LAST_NAME: last_name,
            constants.LOCATION: location,
            constants.USER_ROLE: role
        }
        if not role:
            flash("User role is missing. Please log out and log in again.", 'danger')
            return render_template('profile.html',
                                   mode='edit',
                                   profile=profile_data), 400

        email_error, password_error, first_name_error, last_name_error, location_error = validate_profile_details(
            email, '', '', first_name, last_name, location)

        if email_error or first_name_error or last_name_error or location_error:
            return render_template('profile.html',
                                   mode='edit',
                                   profile=profile_data,
                                   email_error=email_error,
                                   first_name_error=first_name_error,
                                   last_name_error=last_name_error,
                                   location_error=location_error)

        if uploaded_image:
            file_extension = os.path.splitext(uploaded_image.filename)[1]
            folder_path = os.path.join(current_app.root_path, constants.STATIC_IMAGES_PATH)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = constants.USER_PROFILE_IMAGE + '_' + session[constants.USERNAME] + file_extension
            if not allowed_file(filename):
                flash("The uploaded profile image type is not jpg, jpeg, or png.", 'danger')
                return render_template('profile.html',
                                       mode='edit',
                                       profile=profile_data), 400
            filepath = os.path.join(folder_path, filename)
            uploaded_image.save(filepath)
            new_profile_image = os.path.join(constants.STATIC_IMAGES_URL, filename)
        elif delete_image == constants.DELETE_IMAGE_PERFORMED:
            new_profile_image = constants.STATIC_IMAGES_URL + constants.DEFAULT_PROFILE_IMAGE_NAME
        else:
            new_profile_image = profile_image

        try:
            users_repo.update_profile(
                session[constants.USER_ID],
                request.form[constants.EMAIL],
                request.form[constants.FIRST_NAME],
                request.form[constants.LAST_NAME],
                request.form[constants.LOCATION],
                new_profile_image)
            return redirect(url_for(constants.URL_PROFILE))
        except Exception:
            flash("An error occurred while processing your request. Please try again.", 'danger')
            return render_template('profile.html', profile=profile_data), 500

    return render_template('login.html')


def allowed_file(filename):
    """Returns True if the file has an allowed image extension (jpg, jpeg, png)."""
    ext = os.path.splitext(filename)[1].lower()[1:]
    return ext in constants.ALLOWED_IMAGE_EXTENSIONS

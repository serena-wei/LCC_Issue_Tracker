"""Issues blueprint: issue list/create/status and comments."""
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from app import constants, db
from app.decorators import login_and_role_required, login_required

issues_bp = Blueprint('issues', __name__)


@issues_bp.route('/issues', methods=[constants.HTTP_METHOD_GET])
@login_required
def issues():
    """
    Displays issues filtered by status.

    Visitors only see their own issues; helpers and admins see all issues.
    """
    status = request.args.get(constants.ISSUES_STATUS)
    if not status:
        flash("Unable to determine the issue status. Please try again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_ISSUES), constants.HTTP_STATUS_CODE_400

    role = session[constants.USER_ROLE]
    if not role:
        flash("User role is missing. Please log out and log in again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_ISSUES), constants.HTTP_STATUS_CODE_400

    try:
        with db.get_cursor() as cursor:
            if role == constants.USER_ROLE_VISITOR:
                if status == constants.ISSUES_STATUS_RESOLVED:
                    cursor.execute(
                        'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status = %s;',
                        (session[constants.USER_ID], constants.ISSUES_STATUS_RESOLVED))
                else:
                    cursor.execute(
                        'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status != %s;',
                        (session[constants.USER_ID], constants.ISSUES_STATUS_RESOLVED))
            else:
                if status == constants.ISSUES_STATUS_RESOLVED:
                    cursor.execute(
                        'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status = %s;',
                        (constants.ISSUES_STATUS_RESOLVED,))
                else:
                    cursor.execute(
                        'SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status != %s;',
                        (constants.ISSUES_STATUS_RESOLVED,))
            issues_list = cursor.fetchall()
            return render_template(constants.TEMPLATE_ISSUES, issues=issues_list)
    except Exception:
        flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_ISSUES), constants.HTTP_STATUS_CODE_500


@issues_bp.route('/issues/insert', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def issues_insert():
    """
    Creates a new issue.

    - GET: Renders the issue creation form.
    - POST: Validates and inserts the issue, then redirects to the issues list.
    """
    summary_error = None
    if (request.method == constants.HTTP_METHOD_POST
            and constants.ISSUES_SUMMARY in request.form
            and constants.ISSUES_DESCRIPTION in request.form):
        summary = request.form[constants.ISSUES_SUMMARY]
        description = request.form[constants.ISSUES_DESCRIPTION]
        status = request.form[constants.ISSUES_STATUS]
        error_messages = []
        if not description:
            error_messages.append("Description cannot be empty.")
        if not summary:
            error_messages.append("Summary  cannot be empty.")
        if error_messages:
            flash(" ".join(error_messages), constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_ISSUES_INSERT), constants.HTTP_STATUS_CODE_400
        if len(summary) > 255:
            summary_error = "Summary cannot exceed 255 characters."
            return render_template(constants.TEMPLATE_ISSUES_INSERT,
                                   summary=summary,
                                   description=description,
                                   summary_error=summary_error)
        else:
            try:
                with db.get_cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO issues (summary, description, user_id, status) VALUES (%s, %s, %s, %s);',
                        (summary, description, session[constants.USER_ID], constants.ISSUES_STATUS_NEW))
                return redirect(url_for(constants.URL_ISSUES, status=status))
            except Exception:
                flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
                return render_template(constants.TEMPLATE_ISSUES_INSERT), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_ISSUES_INSERT)


@issues_bp.route('/issue/changestatus', methods=['POST'])
@login_and_role_required([constants.USER_ROLE_ADMIN, constants.USER_ROLE_HELPER])
def change_status():
    """Updates an issue's status (admin or helper only)."""
    data = request.get_json()
    issue_id = data.get(constants.ISSUES_ID)
    new_status = data.get(constants.ISSUES_STATUS)
    if not issue_id or not new_status:
        return jsonify({'error': 'Missing issue_id or status'}), constants.HTTP_STATUS_CODE_400

    try:
        with db.get_cursor() as cursor:
            cursor.execute('UPDATE issues SET status = %s WHERE issue_id = %s;', (new_status, issue_id))
        return jsonify({"message": "Status updated successfully."})
    except Exception:
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500


@issues_bp.route('/comments', methods=[constants.HTTP_METHOD_GET])
@login_required
def comments():
    """Displays comments for a specific issue."""
    issue_id = request.args.get(constants.ISSUES_ID)
    if not issue_id:
        flash("Unable to retrieve the current issue.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_COMMENTS), constants.HTTP_STATUS_CODE_400

    try:
        with db.get_cursor() as cursor:
            cursor.execute(
                'SELECT c.comment_id, c.content, c.created_at, u.username, u.profile_image, u.role '
                'FROM comments c '
                'LEFT JOIN users u on u.user_id = c.user_id '
                'WHERE c.issue_id = %s;',
                (issue_id,))
            comments_list = cursor.fetchall()
    except Exception:
        flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_COMMENTS), constants.HTTP_STATUS_CODE_500

    return render_template(
        constants.TEMPLATE_COMMENTS,
        issue_id=issue_id,
        status=request.args.get(constants.ISSUES_STATUS),
        comments=comments_list)


@issues_bp.route('/comments/insert', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def comments_insert():
    """
    Inserts a new comment on an issue.

    - GET: Renders the comment form.
    - POST: Saves the comment; helpers/admins also set the issue status to open.
    """
    if request.method == constants.HTTP_METHOD_POST:
        issue_id = request.form.get(constants.ISSUES_ID)
        issue_status = request.form.get(constants.ISSUES_STATUS)
        content = request.form.get(constants.COMMENTS_CONTENT)
        error_messages = []
        if not issue_id:
            error_messages.append("Please select an issue before adding a comment.")
        if not content:
            error_messages.append("Comment content cannot be empty.")
        if error_messages:
            flash(" ".join(error_messages), constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_COMMENTS_INSERT), constants.HTTP_STATUS_CODE_400

        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    'INSERT INTO comments (issue_id, user_id, content) VALUES (%s, %s, %s);',
                    (issue_id, session[constants.USER_ID], content)
                )

            # Helper/admin comments reopen the issue
            if session[constants.USER_ROLE] in [constants.USER_ROLE_HELPER, constants.USER_ROLE_ADMIN]:
                with db.get_cursor() as cursor:
                    cursor.execute(
                        'UPDATE issues SET status = %s WHERE issue_id = %s;',
                        (constants.ISSUES_STATUS_OPEN, issue_id)
                    )
            return redirect(url_for(constants.URL_COMMENTS, issue_id=issue_id, status=issue_status))
        except Exception:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_COMMENTS_INSERT), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_COMMENTS_INSERT)

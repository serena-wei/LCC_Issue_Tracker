"""Issues blueprint: issue list/create/status and comments."""
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from app import constants
from app.decorators import login_and_role_required, login_required
from app.repositories import comments as comments_repo
from app.repositories import issues as issues_repo

issues_bp = Blueprint('issues', __name__)


@issues_bp.route('/issues', methods=['GET'])
@login_required
def issues():
    """
    Displays issues filtered by status.

    Visitors only see their own issues; helpers and admins see all issues.
    """
    status = request.args.get(constants.ISSUES_STATUS)
    if not status:
        flash("Unable to determine the issue status. Please try again.", 'danger')
        return render_template('issues.html'), 400

    role = session[constants.USER_ROLE]
    if not role:
        flash("User role is missing. Please log out and log in again.", 'danger')
        return render_template('issues.html'), 400

    try:
        issues_list = issues_repo.list_for_role(role, session[constants.USER_ID], status)
        return render_template('issues.html', issues=issues_list)
    except Exception:
        flash("An error occurred while processing your request. Please try again.", 'danger')
        return render_template('issues.html'), 500


@issues_bp.route('/issues/insert', methods=['GET', 'POST'])
@login_required
def issues_insert():
    """
    Creates a new issue.

    - GET: Renders the issue creation form.
    - POST: Validates and inserts the issue, then redirects to the issues list.
    """
    summary_error = None
    if (request.method == 'POST'
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
            flash(" ".join(error_messages), 'danger')
            return render_template('issues_insert.html'), 400
        if len(summary) > 255:
            summary_error = "Summary cannot exceed 255 characters."
            return render_template('issues_insert.html',
                                   summary=summary,
                                   description=description,
                                   summary_error=summary_error)

        try:
            issues_repo.create(summary, description, session[constants.USER_ID])
            return redirect(url_for(constants.URL_ISSUES, status=status))
        except Exception:
            flash("An error occurred while processing your request. Please try again.", 'danger')
            return render_template('issues_insert.html'), 500

    return render_template('issues_insert.html')


@issues_bp.route('/issue/changestatus', methods=['POST'])
@login_and_role_required([constants.USER_ROLE_ADMIN, constants.USER_ROLE_HELPER])
def change_status():
    """Updates an issue's status (admin or helper only)."""
    data = request.get_json()
    issue_id = data.get(constants.ISSUES_ID)
    new_status = data.get(constants.ISSUES_STATUS)
    if not issue_id or not new_status:
        return jsonify({'error': 'Missing issue_id or status'}), 400

    try:
        issues_repo.update_status(issue_id, new_status)
        return jsonify({"message": "Status updated successfully."})
    except Exception:
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500


@issues_bp.route('/comments', methods=['GET'])
@login_required
def comments():
    """Displays comments for a specific issue."""
    issue_id = request.args.get(constants.ISSUES_ID)
    if not issue_id:
        flash("Unable to retrieve the current issue.", 'danger')
        return render_template('comments.html'), 400

    try:
        comments_list = comments_repo.list_for_issue(issue_id)
    except Exception:
        flash("An error occurred while processing your request. Please try again.", 'danger')
        return render_template('comments.html'), 500

    return render_template(
        'comments.html',
        issue_id=issue_id,
        status=request.args.get(constants.ISSUES_STATUS),
        comments=comments_list)


@issues_bp.route('/comments/insert', methods=['GET', 'POST'])
@login_required
def comments_insert():
    """
    Inserts a new comment on an issue.

    - GET: Renders the comment form.
    - POST: Saves the comment; helpers/admins also set the issue status to open.
    """
    if request.method == 'POST':
        issue_id = request.form.get(constants.ISSUES_ID)
        issue_status = request.form.get(constants.ISSUES_STATUS)
        content = request.form.get(constants.COMMENTS_CONTENT)
        error_messages = []
        if not issue_id:
            error_messages.append("Please select an issue before adding a comment.")
        if not content:
            error_messages.append("Comment content cannot be empty.")
        if error_messages:
            flash(" ".join(error_messages), 'danger')
            return render_template('comments_insert.html'), 400

        try:
            comments_repo.create(issue_id, session[constants.USER_ID], content)
            # Helper/admin comments reopen the issue
            if session[constants.USER_ROLE] in [constants.USER_ROLE_HELPER, constants.USER_ROLE_ADMIN]:
                issues_repo.update_status(issue_id, constants.ISSUES_STATUS_OPEN)
            return redirect(url_for(constants.URL_COMMENTS, issue_id=issue_id, status=issue_status))
        except Exception:
            flash("An error occurred while processing your request. Please try again.", 'danger')
            return render_template('comments_insert.html'), 500

    return render_template('comments_insert.html')

"""Routes for viewing and inserting comments on issues."""
from app import app, db, constants
from flask import redirect, render_template, session, url_for, flash, request
from .decorators import login_required

@app.route('/comments', methods=[constants.HTTP_METHOD_GET])
@login_required
def comments():
    """Displays comments for a specific issue."""
    issue_id = request.args.get(constants.ISSUES_ID)
    if not issue_id:
        flash("Unable to retrieve the current issue.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_COMMENTS), constants.HTTP_STATUS_CODE_400
    
    try:
        with db.get_cursor() as cursor:
            cursor.execute('SELECT c.comment_id, c.content, c.created_at, u.username, u.profile_image, u.role '
                        'FROM comments c '
                        'LEFT JOIN users u on u.user_id = c.user_id '
                        'WHERE c.issue_id = %s;',
                        (issue_id,))
            comments = cursor.fetchall()
    except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_COMMENTS), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_COMMENTS, issue_id=issue_id, status=request.args.get(constants.ISSUES_STATUS), comments=comments) 

@app.route('/comments/insert', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
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
            return redirect(url_for(constants.URL_COMMENTS, issue_id=issue_id,status = issue_status))
        except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_COMMENTS_INSERT), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_COMMENTS_INSERT)

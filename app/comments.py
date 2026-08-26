"""
Module: Comments Routes

This module handles comments related to issues in the application. 

It provides routes to:
- Display comments for a specific issue.
- Insert new comments into the database.

Both routes require user authentication. The module also ensures proper validation, error handling, and status updates for issues when necessary.
"""
from app import app, db, constants
from flask import redirect, render_template, session, url_for, flash, request
# Importing decorators from the current package
from .decorators import login_required

@app.route('/comments', methods=[constants.HTTP_METHOD_GET])
@login_required
def comments():
    """
    Handles both GET and POST requests for displaying and adding comments for a specific issue.

    If the user is not logged in, they are redirected to the login page.
    The function retrieves the issue ID from the query parameters, validates it, and fetches comments related to that issue.
    If the issue ID is missing or invalid, a flash message is shown to the user and the HTTP status code 400 is returned.
    If an error occurs while fetching comments from the database, an error message is shown, and HTTP status code 500 is returned.
    
    Returns:
        - Renders the comments page with the relevant data if successful.
        - Flash message and appropriate HTTP status code if there's an error.
    """
    issue_id = request.args.get(constants.ISSUES_ID)
    if not issue_id:
        flash("Unable to retrieve the current issue.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_COMMENTS), constants.HTTP_STATUS_CODE_400
    
    try:
        # Fetch comments from the database based on issue_id.
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
    Handles the insertion of a new comment on an issue.

    This route handles both GET and POST requests. When a GET request is made, it returns
    the comment insertion form. When a POST request is made, it processes the submitted form.
    
    - If the user is not logged in, they are redirected to the login page.
    - If required fields (issue_id or content) are missing, an error message is flashed
      and a 400 HTTP status is returned.
    - If the form submission is valid, the comment is inserted into the database.
    - If the current user is an admin or helper, the status of the associated issue is updated to 'open'.
    - If there is a database error, an error message is logged and flashed to the user, 
      and a 500 HTTP status is returned.

    Returns:
        - On GET request: Renders the comment insertion form.
        - On POST request: Redirects to the comments page or returns error statuses if any issues occur.
    """
    if request.method == constants.HTTP_METHOD_POST:
        issue_id = request.form.get(constants.ISSUES_ID)
        issue_status = request.form.get(constants.ISSUES_STATUS)
        content = request.form.get(constants.COMMENTS_CONTENT)
        # If either field is missing, show an error message and return HTTP 400.
        error_messages = []
        if not issue_id:
            error_messages.append("Please select an issue before adding a comment.")
        if not content:
            error_messages.append("Comment content cannot be empty.")
        if error_messages:
            flash(" ".join(error_messages), constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_COMMENTS_INSERT), constants.HTTP_STATUS_CODE_400

        try:
            # Insert the comment into the database.
            with db.get_cursor() as cursor:
                cursor.execute(
                    'INSERT INTO comments (issue_id, user_id, content) VALUES (%s, %s, %s);',
                    (issue_id, session[constants.USER_ID], content)
                )
                
            # If the current user is a helper or admin, change the issue status to "open".
            if session[constants.USER_ROLE] in [constants.USER_ROLE_HELPER, constants.USER_ROLE_ADMIN]:
                with db.get_cursor() as cursor:
                    cursor.execute(
                        'UPDATE issues SET status = %s WHERE issue_id = %s;',
                        (constants.ISSUES_STATUS_OPEN, issue_id)
                    )
            # Redirect to the comments page for the issue.
            return redirect(url_for(constants.URL_COMMENTS, issue_id=issue_id,status = issue_status))
        except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_COMMENTS_INSERT), constants.HTTP_STATUS_CODE_500

    return render_template(constants.TEMPLATE_COMMENTS_INSERT)

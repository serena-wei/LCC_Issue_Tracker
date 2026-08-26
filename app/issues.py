"""
This module handles routes for managing issues, including viewing, creating, and updating issues. 
It ensures users are authenticated before accessing these routes and checks their roles for 
certain actions.
"""
from app import app, db, constants
from flask import redirect, request, render_template, session, url_for, flash, jsonify
# Importing decorators from the current package
from .decorators import login_required, login_and_role_required

@app.route('/issues', methods=[constants.HTTP_METHOD_GET])
@login_required
def issues():
     """
     Handles GET requests for displaying issues based on their status.

     This function checks if the user is logged in, validates the user role, and retrieves the 
     list of issues from the database based on the status parameter. The function differentiates 
     the results based on the user's role (Visitor or others). If the status parameter is missing 
     or invalid, a flash message is shown and HTTP status code 400 is returned. If an error occurs 
     during the database query, a flash message is displayed and HTTP status code 500 is returned.

     Returns:
          - Renders the issues page with the list of issues if successful.
          - A flash message and appropriate HTTP status code if there's an error.
     """
     # Get the URL parameter status(the status of the issues).
     status = request.args.get(constants.ISSUES_STATUS)
     if not status:
          flash("Unable to determine the issue status. Please try again.", constants.FLASH_MESSAGE_DANGER)
          return render_template(constants.TEMPLATE_ISSUES), constants.HTTP_STATUS_CODE_400

     # Get the user role from the session.
     role = session[constants.USER_ROLE]
     if not role:
        flash("User role is missing. Please log out and log in again.", constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_ISSUES), constants.HTTP_STATUS_CODE_400
     
     try:
          with db.get_cursor() as cursor:
               if role == constants.USER_ROLE_VISITOR:
                    # If the user is a visitor, show issues that are resolved or not resolved based on the status.
                    if status == constants.ISSUES_STATUS_RESOLVED:
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status = %s;',
                              (session[constants.USER_ID], constants.ISSUES_STATUS_RESOLVED))
                    else:
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status != %s;',
                              (session[constants.USER_ID], constants.ISSUES_STATUS_RESOLVED))
               else:
                    # If the user is not a visitor, show issues based on the status for all users.
                    if status == constants.ISSUES_STATUS_RESOLVED:
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status = %s;',
                              (constants.ISSUES_STATUS_RESOLVED,))
                    else:
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status != %s;',
                              (constants.ISSUES_STATUS_RESOLVED,))
               issues = cursor.fetchall()
               return render_template(constants.TEMPLATE_ISSUES, issues=issues)
     except Exception as e:
            # In case of an error, flash an error message and return HTTP status 500.
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_ISSUES), constants.HTTP_STATUS_CODE_500

@app.route('/issues/insert', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def issues_insert():
     """
     Handles the insertion of a new issue into the database.
     
     This route handles both GET and POST requests. On GET requests, it renders the issue 
     creation form. On POST requests, it validates the input data (summary and description) 
     and inserts the new issue into the database if the data is valid. Flash messages are used 
     to notify the user of any validation errors or issues during the insertion process.

     Returns:
          - On GET request: Renders the issue creation form.
          - On POST request: 
               - If validation passes: Redirects to the issues page.
               - If validation fails or an error occurs: Renders the issue creation form with error messages.
     """
     summary_error=None
     # Handle POST request: Validate form fields and insert the new issue into the database
     if request.method==constants.HTTP_METHOD_POST and constants.ISSUES_SUMMARY in request.form and constants.ISSUES_DESCRIPTION in request.form:
          summary = request.form[constants.ISSUES_SUMMARY]
          description = request.form[constants.ISSUES_DESCRIPTION]
          status = request.form[constants.ISSUES_STATUS]
          # If either field is missing, show an error message and return HTTP 400.
          error_messages = []
          if not description:
               error_messages.append("Description cannot be empty.")
          if not summary:
               error_messages.append("Summary  cannot be empty.")
          if error_messages:
               flash(" ".join(error_messages), constants.FLASH_MESSAGE_DANGER)
               return render_template(constants.TEMPLATE_ISSUES_INSERT), constants.HTTP_STATUS_CODE_400
          if len(summary)>255:
               summary_error="Summary cannot exceed 255 characters."
               return render_template(constants.TEMPLATE_ISSUES_INSERT,
                                   summary=summary,
                                   description=description,
                                   summary_error=summary_error
                                   )
          else:
               try:
                    with db.get_cursor() as cursor:
                         cursor.execute('INSERT INTO issues (summary, description, user_id, status) VALUES (%s, %s, %s, %s);',
                                   (summary, description, session[constants.USER_ID], constants.ISSUES_STATUS_NEW))
                    return redirect(url_for(constants.URL_ISSUES, status=status))
               except Exception as e:
                    flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
                    return render_template(constants.TEMPLATE_ISSUES_INSERT), constants.HTTP_STATUS_CODE_500

     # If the request method is GET, render the issue creation form     
     return render_template(constants.TEMPLATE_ISSUES_INSERT) 

@app.route('/issue/changestatus', methods=['POST'])
@login_and_role_required([constants.USER_ROLE_ADMIN, constants.USER_ROLE_HELPER])
def change_status():
    """
    This route allows an authenticated user with the role of 'admin' or 'helper'
    to update the status of an issue in the database. If the user is not logged in 
    or does not have the appropriate permissions, they will be redirected or denied access.
    
    Returns:
        - A success message if the status update is successful.
        - An error message if the request is missing required data or an exception occurs.
    """
    data = request.get_json()
    issue_id = data.get(constants.ISSUES_ID)
    new_status = data.get(constants.ISSUES_STATUS)
    if not issue_id or not new_status:
        return jsonify({'error': 'Missing issue_id or status'}), constants.HTTP_STATUS_CODE_400
    
    try:
        with db.get_cursor() as cursor:
          cursor.execute('UPDATE issues SET status = %s WHERE issue_id = %s;', (new_status, issue_id))
        return jsonify({"message": "Status updated successfully."})
    except Exception as e:
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500
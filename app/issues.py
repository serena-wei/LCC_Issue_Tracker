"""Routes for viewing, creating, and updating issues."""
from app import app, db, constants
from flask import redirect, request, render_template, session, url_for, flash, jsonify
from .decorators import login_required, login_and_role_required

@app.route('/issues', methods=[constants.HTTP_METHOD_GET])
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
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status = %s;',
                              (session[constants.USER_ID], constants.ISSUES_STATUS_RESOLVED))
                    else:
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.user_id = %s AND i.status != %s;',
                              (session[constants.USER_ID], constants.ISSUES_STATUS_RESOLVED))
               else:
                    if status == constants.ISSUES_STATUS_RESOLVED:
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status = %s;',
                              (constants.ISSUES_STATUS_RESOLVED,))
                    else:
                         cursor.execute('SELECT i.issue_id, i.summary, i.description, i.created_at, i.status FROM issues i WHERE i.status != %s;',
                              (constants.ISSUES_STATUS_RESOLVED,))
               issues = cursor.fetchall()
               return render_template(constants.TEMPLATE_ISSUES, issues=issues)
     except Exception as e:
            flash("An error occurred while processing your request. Please try again.", constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_ISSUES), constants.HTTP_STATUS_CODE_500

@app.route('/issues/insert', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def issues_insert():
     """
     Creates a new issue.

     - GET: Renders the issue creation form.
     - POST: Validates and inserts the issue, then redirects to the issues list.
     """
     summary_error=None
     if request.method==constants.HTTP_METHOD_POST and constants.ISSUES_SUMMARY in request.form and constants.ISSUES_DESCRIPTION in request.form:
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

     return render_template(constants.TEMPLATE_ISSUES_INSERT) 

@app.route('/issue/changestatus', methods=['POST'])
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
    except Exception as e:
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), constants.HTTP_STATUS_CODE_500

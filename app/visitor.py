"""
Module: Visitor Home Route

This module defines the endpoint for the visitor homepage in the login application.
It includes role-based access control to ensure only visitor users can access this page.
Unauthorized users are either redirected or shown a 403 error.
"""
from app import app, db, constants
from flask import redirect, render_template, session, url_for
# Importing decorators from the current package
from .decorators import role_required

@app.route('/visitor/home')
@role_required(constants.USER_ROLE_VISITOR)
def visitor_home():
     """Visitor Homepage endpoint.

     Methods:
     - get: Renders the homepage for the current visitor, or an "Access
          Denied" 403: Forbidden page if the current user has a different role.

     If the user is not logged in, requests will redirect to the login page.
     """
     return render_template(constants.TEMPLATE_VISITOR_HOME)
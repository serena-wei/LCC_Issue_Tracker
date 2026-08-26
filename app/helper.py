"""
Module: Helper Home Route

This module defines the endpoint for the helper homepage in the login application.
It includes role-based access control to ensure only helper users can access this page.
Unauthorized users are either redirected or shown a 403 error.
"""
from app import app, db, constants
from flask import redirect, render_template, session, url_for
# Importing decorators from the current package
from .decorators import role_required

@app.route('/helper/home')
@role_required(constants.USER_ROLE_HELPER)
def helper_home():
     """Helper Homepage endpoint.

     Methods:
     - get: Renders the homepage for the current helper user, or an "Access
          Denied" 403: Forbidden page if the current user has a different role.

     If the user is not logged in, requests will redirect to the login page.
     """
     return render_template(constants.TEMPLATE_HELPER_HOME)
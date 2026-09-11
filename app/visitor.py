"""Visitor homepage route with role-based access control."""
from app import app, db, constants
from flask import redirect, render_template, session, url_for
from .decorators import role_required

@app.route('/visitor/home')
@role_required(constants.USER_ROLE_VISITOR)
def visitor_home():
     """Renders the visitor homepage."""
     return render_template(constants.TEMPLATE_VISITOR_HOME)

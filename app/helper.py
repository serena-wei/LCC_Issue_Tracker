"""Helper homepage route with role-based access control."""
from app import app, db, constants
from flask import redirect, render_template, session, url_for
from .decorators import role_required

@app.route('/helper/home')
@role_required(constants.USER_ROLE_HELPER)
def helper_home():
     """Renders the helper homepage."""
     return render_template(constants.TEMPLATE_HELPER_HOME)

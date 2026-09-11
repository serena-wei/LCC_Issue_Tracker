"""Admin homepage route with role-based access control."""
from app import app, db, constants
from flask import redirect, render_template, session, url_for
from .decorators import role_required

@app.route('/admin/home')
@role_required(constants.USER_ROLE_ADMIN)
def admin_home():
     """Renders the admin homepage."""
     return render_template(constants.TEMPLATE_ADMIN_HOME)

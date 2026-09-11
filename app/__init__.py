from flask import Flask

app = Flask(__name__)

# Anyone with access to this key can pretend to be signed in as any user.
app.secret_key = 'Example Secret Key (CHANGE THIS TO YOUR OWN SECRET KEY!)'

from app import connect
from app import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)

from app import user
from app import visitor
from app import helper
from app import admin
from app import issues
from app import comments
from app import profile
from app import constants

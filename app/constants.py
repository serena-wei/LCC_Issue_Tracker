"""Domain constants: roles, statuses, field keys, endpoints, and shared paths."""
import os

SESSION_LOGGED_IN = 'loggedin'

# Field / session / JSON keys (aligned with DB columns and forms)
USER_ID = 'user_id'
USERNAME = 'username'
USER_ROLE = 'role'
USER_STATUS = 'status'
PASSWORD = 'password'
PASSWORD_HASH = 'password_hash'
CONFIRM_PASSWORD = 'confirm_password'
EMAIL = 'email'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
LOCATION = 'location'
USER_PROFILE_IMAGE = 'profile_image'
USER_IDS = 'user_ids'

ISSUES_ID = 'issue_id'
ISSUES_STATUS = 'status'
ISSUES_SUMMARY = 'summary'
ISSUES_DESCRIPTION = 'description'

COMMENTS_CONTENT = 'content'

USER_ROLE_VISITOR = 'visitor'
USER_ROLE_HELPER = 'helper'
USER_ROLE_ADMIN = 'admin'

USER_STATUS_ACTIVE = 'active'
USER_STATUS_INACTIVE = 'inactive'

ISSUES_STATUS_RESOLVED = 'resolved'
ISSUES_STATUS_NEW = 'new'
ISSUES_STATUS_OPEN = 'open'

# Profile image deletion flag: '0' = not deleted, '1' = deleted
DELETE_IMAGE = 'delete_image'
DELETE_IMAGE_PERFORMED = '1'
DELETE_IMAGE_NOT_PERFORMED = '0'

URL_LOGIN = 'auth.login'
URL_LOGOUT = 'auth.logout'
URL_SIGNUP = 'auth.signup'
URL_RESETPASSWORD = 'auth.resetpassword'
URL_COMMENTS = 'issues.comments'
URL_ISSUES = 'issues.issues'
URL_PROFILE = 'users.profile'
URL_USER_LIST = 'users.user_list'
URL_VISITOR_HOME = 'users.visitor_home'
URL_HELPER_HOME = 'users.helper_home'
URL_ADMIN_HOME = 'users.admin_home'

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
USERNAME_PATTERN = r'^[A-Za-z0-9]+$'

DEFAULT_PROFILE_IMAGE_NAME = '/default_profile_image.jpg'
STATIC_FOLDER = 'static'
IMAGES_FOLDER = 'images'
STATIC_IMAGES_PATH = os.path.join(STATIC_FOLDER, IMAGES_FOLDER)
STATIC_IMAGES_URL = f'/{STATIC_FOLDER}/{IMAGES_FOLDER}'
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}

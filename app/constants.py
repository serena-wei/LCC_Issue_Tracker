"""
Application-wide constants for roles, status codes, templates,
database field names, and file paths.
"""
import os

SESSION_LOGGED_IN = 'loggedin'

HTTP_METHOD_POST = 'POST'
HTTP_METHOD_GET = 'GET'

USER_ROLE_VISITOR = 'visitor'
USER_ROLE_HELPER = 'helper'
USER_ROLE_ADMIN = 'admin'

USER_ID = 'user_id'
USERNAME = 'username'
USER_ROLE = 'role'
EMAIL = 'email'
PASSWORD = 'password'
PASSWORD_HASH = 'password_hash'
CONFIRM_PASSWORD = 'confirm_password'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
LOCATION = 'location'
USER_STATUS='status'
USER_PROFILE_IMAGE='profile_image'

USER_IDS_KEY = 'user_ids'
USER_IDS = 'user_ids'

USER_STATUS_ACTIVE = 'active'
USER_STATUS_INACTIVE = 'inactive'

ISSUES_STATUS_RESOLVED='resolved'
ISSUES_STATUS_NEW='new'
ISSUES_STATUS_OPEN = 'open'

ISSUES_SUMMARY='summary'
ISSUES_DESCRIPTION='description'
ISSUES_ID='issue_id'
ISSUES_STATUS='status'

COMMENTS_CONTENT='content'

# Profile image deletion flag: '0' = not deleted, '1' = deleted
DELETE_IMAGE='delete_image'
DELETE_IMAGE_PERFORMED='1'
DELETE_IMAGE_NOT_PERFORMED='0'

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

TEMPLATE_ACCESS_DENIED = 'access_denied.html'
TEMPLATE_ADMIN_HOME = 'admin_home.html'
TEMPLATE_HELPER_HOME = 'helper_home.html'
TEMPLATE_VISITOR_HOME = 'visitor_home.html'
TEMPLATE_COMMENTS = 'comments.html'
TEMPLATE_COMMENTS_INSERT = 'comments_insert.html'
TEMPLATE_ISSUES = 'issues.html'
TEMPLATE_ISSUES_INSERT = 'issues_insert.html'
TEMPLATE_PROFILE = 'profile.html'
TEMPLATE_LOGIN= 'login.html'
TEMPLATE_SIGNUP = 'signup.html'
TEMPLATE_RESETPASSWORD = 'resetpassword.html'
TEMPLATE_USER_LIST = 'user_list.html'

HTTP_STATUS_CODE_403 = 403
HTTP_STATUS_CODE_400 = 400
HTTP_STATUS_CODE_500 = 500
HTTP_STATUS_CODE_404 = 404

FLASH_MESSAGE_DANGER = 'danger'

URL_PARAMETER_MODE = 'mode'
URL_PARAMETER_MODE_EDIT = 'edit'

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
USERNAME_PATTERN = r'^[A-Za-z0-9]+$'

DEFAULT_PROFILE_IMAGE_NAME = '/default_profile_image.jpg'
STATIC_FOLDER = 'static'
IMAGES_FOLDER = 'images'
STATIC_IMAGES_PATH = os.path.join(STATIC_FOLDER, IMAGES_FOLDER)
STATIC_IMAGES_URL = f'/{STATIC_FOLDER}/{IMAGES_FOLDER}'
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}

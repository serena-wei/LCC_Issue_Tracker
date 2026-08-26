"""
constants.py

This module defines various constants used throughout the application, 
including HTTP methods, user roles, status codes, template names, 
database field names, and file paths.

It helps maintain consistency and avoids hardcoding values in multiple places.
"""
import os

# Used to indicate whether the user is logged in in the session
SESSION_LOGGED_IN = 'loggedin'

HTTP_METHOD_POST = 'POST'
HTTP_METHOD_GET = 'GET'

# Role to new users upon registration.
USER_ROLE_VISITOR = 'visitor'
USER_ROLE_HELPER = 'helper'
USER_ROLE_ADMIN = 'admin'
USER_ROLE_PROFILE = 'profile'

# User information fields
USER_ID = 'user_id'  # Unique identifier for the user
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

# Define the constant for 'user_ids' key
USER_IDS_KEY = 'user_ids'

USER_IDS = 'user_ids' 

# user status
USER_STATUS_ACTIVE = 'active'
USER_STATUS_INACTIVE = 'inactive'

# Issues' status
ISSUES_STATUS_RESOLVED='resolved'
ISSUES_STATUS_NEW='new'
ISSUES_STATUS_OPEN = 'open'

# issues information fields
ISSUES_SUMMARY='summary'
ISSUES_DESCRIPTION='description'
ISSUES_ID='issue_id'
ISSUES_STATUS='status'

# comments information fields
COMMENTS_CONTENT='content'

# Determine whether the user profile picture deletion operation has been performed: 0: Not performed; 1: Performed.
DELETE_IMAGE='delete_image'
DELETE_IMAGE_PERFORMED='1'
DELETE_IMAGE_NOT_PERFORMED='0'

# URL endpoint names
URL_LOGIN = 'login'  # URL for the login page
URL_COMMENTS = 'comments'  # URL for the comments page related to an issue
URL_ISSUES = 'issues'  # URL for the issues page,
URL_VISITOR_HOME = 'visitor_home'
URL_HELPER_HOME = 'helper_home'
URL_ADMIN_HOME = 'admin_home'

# Template file names
TEMPLATE_ACCESS_DENIED = 'access_denied.html'  # Template displayed when a user is denied access to a resource
TEMPLATE_ADMIN_HOME = 'admin_home.html'  # Template for the admin home page
TEMPLATE_HELPER_HOME = 'helper_home.html'  # Template for the helper home page
TEMPLATE_VISITOR_HOME = 'visitor_home.html'  # Template for the visitor home page
TEMPLATE_COMMENTS = 'comments.html'  # Template for displaying comments related to an issue
TEMPLATE_COMMENTS_INSERT = 'comments_insert.html'  # Template for inserting a new comment
TEMPLATE_ISSUES = 'issues.html'  # Template for displaying the list of issues
TEMPLATE_ISSUES_INSERT = 'issues_insert.html'  # Template for inserting a new issue
TEMPLATE_PROFILE = 'profile.html'  # Template for displaying the profile details
TEMPLATE_LOGIN= 'login.html'
TEMPLATE_SIGNUP = 'signup.html'
TEMPLATE_RESETPASSWORD = 'resetpassword.html'
TEMPLATE_USER_LIST = 'user_list.html'

# HTTP status codes
# User permission-related issues
HTTP_STATUS_CODE_403 = 403  # Forbidden: User does not have permission to access the requested resource
# Parameter-related errors (e.g., missing or invalid input)
HTTP_STATUS_CODE_400 = 400  # Bad Request: The server could not understand the request due to invalid syntax or missing parameters
# Database errors or other internal server issues
HTTP_STATUS_CODE_500 = 500  # Internal Server Error: A generic error indicating that something went wrong on the server side
HTTP_STATUS_CODE_404 = 404  # Indicates that the requested data could not be found in the database.

# Flash message types for different scenarios
FLASH_MESSAGE_DANGER = 'danger' # Used for error messages or warnings

# Constant for the 'mode' parameter in the URL,(default to an empty string if not provided)
URL_PARAMETER_MODE = 'mode' # Distinguish between viewing and editing operations
URL_PARAMETER_MODE_EDIT = 'edit'  # Page can edit

# Regular expression for validating an email address.
# Explanation:
# ^                 : Start of the string
# [a-zA-Z0-9_.+-]+  : Local part (before '@'), allows letters, numbers, and some special characters (_ . + -)
# @                 : Must contain '@' symbol
# [a-zA-Z0-9-]+     : Domain name (e.g., example)
# \.                : Must contain a dot (.)
# [a-zA-Z0-9-.]+    : Domain extension (e.g., com, co.nz), allowing multiple subdomains
# $                 : End of the string
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
# In constants.py, define the regex pattern for username validation
USERNAME_PATTERN = r'^[A-Za-z0-9]+$'  # Only allows letters (A-Z, a-z) and numbers (0-9)

# Default profile image name
DEFAULT_PROFILE_IMAGE_NAME = '/default_profile_image.jpg'
# Static folder paths
STATIC_FOLDER = 'static'  # Root folder for static resources
IMAGES_FOLDER = 'images'  # Folder for storing user-uploaded images
# Server-side file storage path (used for constructing absolute paths)
STATIC_IMAGES_PATH = os.path.join(STATIC_FOLDER, IMAGES_FOLDER)  
# Web-accessible path (used for displaying images on the frontend)
STATIC_IMAGES_URL = f'/{STATIC_FOLDER}/{IMAGES_FOLDER}'
# 在你的代码中，检查上传的文件是否是图片类型
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
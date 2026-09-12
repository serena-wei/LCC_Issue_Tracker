"""Application configuration loaded from environment variables."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Always load project-root .env (WSGI cwd may not be the project folder).
# override=False: values already set in the process (e.g. PythonAnywhere WSGI)
# win over .env, so deploy credentials are not replaced by a stale .env file.
_ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(_ENV_PATH, override=False)


class Config:
    """Flask and database settings from the environment."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-change-me')

    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'lcc_issue_tracker_db')

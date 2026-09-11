"""Application configuration loaded from environment variables."""
import os

from dotenv import load_dotenv

# Load local .env if present (never commit real secrets).
load_dotenv()


class Config:
    """Flask and database settings from the environment."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-change-me')

    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'lcc_issue_tracker_db')

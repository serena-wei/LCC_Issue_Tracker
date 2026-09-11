"""Launcher for the LCC Issue Tracker Flask app.

Prefer this script for local development. On WSGI servers you can import
`app` from this module or directly from the `app` package.
"""
from app import app

if __name__ == "__main__":
    app.run(debug=True)

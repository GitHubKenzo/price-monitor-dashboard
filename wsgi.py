# wsgi.py
"""
WSGI entrypoint for Gunicorn.
Dash exposes the underlying Flask server as `app.server`.
"""

from app import app

# Gunicorn が参照する WSGI アプリ
server = app.server

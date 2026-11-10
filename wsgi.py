"""
WSGI config for freelance_marketplace project.
Root WSGI entrypoint for Render and Gunicorn deployment.
"""
import os
import sys
from pathlib import Path

# Add the actual Django project directory to sys.path
PROJECT_DIR = Path(__file__).resolve().parent / 'freelance_marketplace'
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelance_marketplace.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

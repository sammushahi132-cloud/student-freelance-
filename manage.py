#!/usr/bin/env python
"""
Root convenience wrapper for manage.py
Allows running 'python manage.py runserver' directly from the root workspace directory.
"""
import os
import sys
from pathlib import Path

def main():
    project_dir = Path(__file__).resolve().parent / 'freelance_marketplace'
    sys.path.insert(0, str(project_dir))
    os.chdir(project_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelance_marketplace.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()


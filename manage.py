#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import connection
from user.admin import DATABASES_NAMES


# Make Automatic Migrations if tables doesn't exist
def makemigrations():
    """
        Note - Do Automatic migration
    """
    try:
        os.system("python manage.py makemigrations user")
        os.system("python manage.py migrate user")
    except Exception as error:
        print("Error ocurred during migrations - ", error)


# Need to check for the tables
def check_for_tables():
    """
        Note - Check whether the tables exist in the DATABASE
    """
    all_tables = connection.introspection.table_names()
    is_available =  True
    for dbs in DATABASES_NAMES:
        if dbs not in all_tables:
            is_available = False
    
    if is_available == False:
        makemigrations()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toDo.settings')
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
    # Need to  check as we can automatically do migrations.
    check_for_tables()
    main()


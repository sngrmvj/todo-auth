
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from user.admin import DATABASES_NAMES
import os,sys




def initial_migrations():

    """
        Note - Check whether the tables exist in the DATABASE
    """
    all_tables = connection.introspection.table_names()
    is_available =  True
    for dbs in DATABASES_NAMES:
        if dbs not in all_tables:
            is_available = False
    
    if is_available == False:
        """
            Note - Do Automatic migration
        """
        try:
            os.system("python manage.py makemigrations user")
            os.system("python manage.py migrate user")
            return Response({'message':'DB created successfully'}, status=status.HTTP_201_CREATED,content_type="application/json")
        except Exception as error:
            print(f"Error ocurred during automatic migrations - {error}")
            return Response({'error':f"Error ocurred during automatic migrations  - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")
        
    else:
        return Response({'message':'DB is intact'}, status=status.HTTP_200_OK,content_type="application/json")
    


if __name__ == "__main__":
    """
        Note - This is for the initial migration.
    """
    try:
        initial_migrations()
    except Exception as exception:
        print(f"Exception raised during the initial migration - {exception}")
from toDo.settings import DATABASES
from django.contrib import admin
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
from django.db import connection

import os,sys

# Register your models here.

# List of Global Variables to be used.
GENERATED_OTP = None
REFRESH_TOKEN_NAME = 'todo-refreshToken'
ACCESS_TOKEN_NAME = 'todo-accessToken'
DATABASES_NAMES = ['admin_credentials', 'blacklist_tokens', 'credentials', 'django_migrations', 'register_tokens', 'user_feedback']



#>>>> PING

@api_view(http_method_names=['GET'])
def ping():
    string = "<header style='font-size:20px;color:teal'>Yes you are able to access</header>"
    return Response({"status":string},status=status.HTTP_200_OK,content_type="application/json")

# --------------------------------------------------------------------------------------------------------

#>>>> Automatic Migration

@api_view(http_method_names=['PUT'])
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
    

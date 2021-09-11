from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

import os,sys

# Register your models here.

# List of Global Variables to be used.
GENERATED_OTP = None
REFRESH_TOKEN_NAME = 'todo-refreshToken'
ACCESS_TOKEN_NAME = 'todo-accessToken'
DATABASES_NAMES = ['blacklist_tokens', 'credentials', 'django_migrations', 'register_tokens', 'user_feedback']



#>>>> PING

@api_view(http_method_names=['GET'])
def ping(request):
    string = "Welcome to To-Do Planners"
    return Response({"status":string},status=status.HTTP_200_OK,content_type="application/json")

# --------------------------------------------------------------------------------------------------------

#>>>> Automatic Migration

@api_view(http_method_names=['PUT'])
def admin_migration():
    
    """
        Note - Do Automatic migration by admin
    """
    try:
        os.system("python manage.py makemigrations user")
        os.system("python manage.py migrate user")
        return Response({'message':'DB migration successful'}, status=status.HTTP_201_CREATED,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during automatic migrations - {error}")
        return Response({'error':f"Error ocurred during automatic migrations  - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")
    

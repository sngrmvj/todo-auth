from toDo.settings import DATABASES
from django.contrib import admin
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse

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
    return HttpResponse(string,status=status.HTTP_200_OK,content_type="application/json")

from toDo.settings import DATABASES
from django.contrib import admin

# Register your models here.

# List of Global Variables to be used.
GENERATED_OTP = None
REFRESH_TOKEN_NAME = 'todo-refreshToken'
ACCESS_TOKEN_NAME = 'todo-accessToken'
DATABASES_NAMES = ['admin_credentials', 'blacklist_tokens', 'credentials', 'django_migrations', 'register_tokens', 'user_feedback']

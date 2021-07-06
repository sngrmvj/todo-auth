
from django.urls import path
from user.views import login,signup,token_validation

urlpatterns = [
    path("login",login,name="Login"),
    path("signup",signup,name="SignUp"),
    path("validation",token_validation,name="Validate Token")
]
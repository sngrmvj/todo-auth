
from django.urls import path
from user.views import login,signup,get_access_token,authorization,otp_verify,send_otp

urlpatterns = [
    path("login",login,name="Login"),
    path("register",signup,name="register"),
    path("authorize",authorization,name="Validate Token"),
    path("refresh",get_access_token,name="Get Access Token"),
    path("validate_otp",otp_verify,name="OTP Verification"),
    path("otp",send_otp,name="Send OTP")
]
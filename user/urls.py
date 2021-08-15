
from django.urls import path
from user import views

urlpatterns = [
    path("login",views.login,name="Login"),
    path("register",views.signup,name="register"),
    path("check_authorize",views.check_your_authorization,name="Check Authorisation"),
    path("refresh",views.get_access_token,name="Get Access Token"),
    path("validate_otp",views.otp_verify,name="OTP Verification"),
    path("otp",views.send_otp,name="Send OTP"),
    path("reset",views.change_password,name="Password reset"),
    path("delete",views.delete_user,name="Delete User"),
    path("updateEmail",views.update_user_email,name="Update User Email")
]
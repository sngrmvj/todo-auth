
from django.urls import path
from user import views

urlpatterns = [
    path("login",views.login,name="Login"),
    path("register",views.signup,name="register"),
    path("check_authorize",views.check_your_authorization,name="Check Authorisation"),
    path("get_access",views.get_access_token,name="Get Access Token"),
    path("validate_otp",views.otp_verify,name="OTP Verification"),
    path("otp",views.send_otp,name="Send OTP"),
    # path("reset",views.change_password,name="Password reset"),
    path("delete",views.delete_user_by_admin,name="Delete User"),
    path("account_delete",views.accountDeletion,name="Delete Account"),
    path("updateEmail",views.update_user_email,name="Update User Email"),
    path("lastname",views.update_user_lastname, name= "Update User Lastname"),
    path("firstname",views.update_user_firstname, name= "Update User Firstname"),
    path("change_password_from_profile", views.change_password_profile_page,name = "Change password from profile page"),
    path("makeAdmin",views.makeAdmin, name="Make Admin"),
    path('get_all',views.get_all_user_details, name="Get All User Details"),
    path('get_user',views.get_user, name="Get only one person")
]
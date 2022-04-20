from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import delete_user, get_users_profile, register_users, change_password

urlpatterns = [
    # create a new user with credentials
    path('create', register_users, name="register_user"),
    # obtain a access and refresh token from username and password
    path('token', TokenObtainPairView.as_view(), name='get_token'),
    # obtain a access token from a refresh token
    path('refresh', TokenRefreshView.as_view(), name='refresh_token'),
    # change the password for the current user
    path('change_password', change_password, name="change_password"),
    # change and view the profile info
    path("profile", get_users_profile, name="profile"),
    # delete the current account
    path("delete", delete_user, name="delete_current_user")

]

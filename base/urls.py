from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (delete_user, get_users_profile,
                    register_users, change_password, login_user, update_profile, check_auth,)

urlpatterns: list = [
    # check auth state
    path('check-auth', check_auth, name="check-auth-state"),
    # create a new user with credentials
    path('create', register_users, name="register_user"),
    # obtain a access and refresh token from username and password
    path('token', login_user, name='login_user'),
    # obtain a access token from a refresh token
    path('refresh', TokenRefreshView.as_view(), name='refresh_token'),
    # change the password for the current user
    path('change-password', change_password, name="change_password"),
    # change and view the profile info
    path("profile", get_users_profile, name="profile"),
    # upgrade profile
    path('update-profile', update_profile, name="update-profile"),
    # delete the current account
    path("delete", delete_user, name="delete_current_user")
]

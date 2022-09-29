from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


def get_refresh_tokens(user: User) -> dict[str, str]:
    token = RefreshToken.for_user(user)
    return {
        "refresh": str(token),
        "access": str(token.access_token)
    }

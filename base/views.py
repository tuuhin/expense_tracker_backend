from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, permission_classes, parser_classes)
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from .utils import get_refresh_tokens
from .models import Profile
from .serializers import (ChangePasswordSerializer,
                          ProfileSerializer, UserSerializer)


@api_view(http_method_names=['POST'])
def register_users(request: Request) -> Response:
    user_serializer = UserSerializer(data=request.data)

    if user_serializer.is_valid():
        user_serializer.save()

        token_serilizer = TokenObtainSerializer(data=request.data)
        if token_serilizer.is_valid():

            profile = Profile.objects.filter(user=token_serilizer.user).first()
            profile_serializer = ProfileSerializer(profile, many=False)
            tokens = get_refresh_tokens(token_serilizer.user)

            return Response({'profile': profile_serializer.data, 'tokens': tokens}, status=status.HTTP_201_CREATED)

        return Response(token_serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
def login_user(request: Request) -> Response:

    login_serializer = TokenObtainSerializer(data=request.data)

    if login_serializer.is_valid():

        profile = Profile.objects.get(user=login_serializer.user)
        profile_serializer = ProfileSerializer(profile, many=False)

        tokens = get_refresh_tokens(login_serializer.user)

        return Response({'profile': profile_serializer.data, 'tokens': tokens}, status=status.HTTP_201_CREATED)

    return Response(login_serializer.errors, status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_users_profile(request: Request) -> Response:

    profile = Profile.objects.get(user=request.user)
    profile_serializer = ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile(request: Request) -> Response:
    data = request.data.copy()
    data['user'] = request.user.pk
    profile = Profile.objects.get(user=request.user)
    profile_serializer = ProfileSerializer(profile, data=data)

    if profile_serializer.is_valid():
        profile_serializer.save()

        return Response(profile_serializer.data, status=status.HTTP_202_ACCEPTED)
    print(profile_serializer.errors)
    return Response(profile_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request: Request) -> Response:

    current_user = UserSerializer(request.user)
    user = User.objects.filter(**current_user.data).first()

    if user:
        user.delete()
        return Response({"detail": f"User  has been deleted successfully "},
                        status=status.HTTP_204_NO_CONTENT)

    raise NotFound("No user found with this credentials")


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def change_password(request: Request) -> Response:

    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    old_password = serializer.data.get("old_password")
    new_password = serializer.data.get('new_password')

    if new_password == old_password:
        raise NotAcceptable("Both password found are same.")

    if not user.check_password(old_password):
        raise NotAcceptable("The actual password dosen't match this one")

    if new_password:
        user.set_password(str(new_password))
        user.save()
        return Response({'detail': 'your password has been changed'},
                        status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request: Request) -> Response:
    user = request.user
    tokens = get_refresh_tokens(user)
    return Response(tokens, status=status.HTTP_302_FOUND)

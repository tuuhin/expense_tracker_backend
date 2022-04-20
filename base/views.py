from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .models import Profile
from .serializers import ChangePasswordSerializer, ProfileSerializer, UserSerializer


@api_view(http_method_names=["GET", "PUT"])
@permission_classes([IsAuthenticated])
def get_users_profile(request):

    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        profile_serializer = ProfileSerializer(profile, many=False)

        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        data = request.data.copy()
        data['user'] = request.user.id
        profile = Profile.objects.get(user=request.user)
        profile_serializer = ProfileSerializer(profile, data=data)

        if profile_serializer.is_valid():
            profile_serializer.save()

            return Response(profile_serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(profile_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):

    current_user = UserSerializer(request.user)
    id = current_user.data.get('id')
    user = User.objects.get(pk=id)

    if user:
        user.delete()
        return Response({"message": f"User {user.pk} has been deleted successfully 😢😢"},
                        status=status.HTTP_204_NO_CONTENT)

    return Response({'message': "No user found with this credentials 😕😕"},
                    status=status.HTTP_417_EXPECTATION_FAILED)


@api_view(http_method_names=['POST'])
def register_users(request):

    user = UserSerializer(data=request.data)

    if user.is_valid():
        user.save()
        id = user.data.get("id")
        tokens = user.get_tokens(id)
        return Response({'user': user.data, **tokens}, status=status.HTTP_201_CREATED)

    return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
        old_password = serializer.data.get("old_password")
        if not user.check_password(old_password):
            return Response({
                "message": "Please give a valid password for this account 🤕🤕"
            }, status=status.HTTP_400_BAD_REQUEST)

        new_password = serializer.data.get('new_password')
        if new_password:
            user.set_password(str(new_password))
            user.save()
            return Response({'message': 'your password has been changed 😁😁'},
                            status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

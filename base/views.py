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
        pass


@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    current_user = UserSerializer(request.user)
    user = User.objects.get(pk=current_user.data['id'])
    if user:
        user.delete()
        return Response({"success": f"User {user.pk} has been deleted successfullt"},
                        status=status.HTTP_204_NO_CONTENT)
    return Response({'message': "Can't get the user"}, status=status.HTTP_417_EXPECTATION_FAILED)


@api_view(http_method_names=['POST'])
def register_users(request):
    user = UserSerializer(data=request.data)
    if user.is_valid():
        user.save()
        tokens = user.get_tokens(user.data.get("id"))
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
                "data": "The applied password is a wrong one please apply the correct one "
            }, status=status.HTTP_400_BAD_REQUEST)
        new_password = serializer.data.get('new_password')
        if new_password:
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'data': 'your password has been changed '}, status=status.HTTP_200_OK)
        return Response({'data': 'new_password is not found'}, status=status.HTTP_304_NOT_MODIFIED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

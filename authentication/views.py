from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status


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
    obj = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        old_password = serializer.data.get("old_password")
        if not obj.check_password(old_password):
            return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
        obj.set_password(serializer.data.get('new_password'))
        obj.save()
        return Response({'data': 'changed passoword'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

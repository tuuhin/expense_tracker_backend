from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',)
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True}
        }

    def get_tokens(self, pk):
        current_user = User.objects.get(pk=pk)
        tokens = self._get_tokens_for_user(current_user)
        return tokens

    def _get_tokens_for_user(self, user):
        # get tokens from user data
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},

        }


class ChangePasswordSerializer(serializers.Serializer):

    '''
    Serializer for changing password
    params: `old_password` old password for the user
    params: `new_password` new password for the user
    '''

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

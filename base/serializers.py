from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    # get tokens from user data
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True}
        }

    def get_tokens(self, pk):
        current_user = User.objects.get(pk=pk)
        tokens = get_tokens_for_user(current_user)
        return tokens


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

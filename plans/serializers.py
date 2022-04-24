from rest_framework import serializers
from .models import Goal, Saving


class GoalSerializers(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'collected': {'required': True}
        }


class SavingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Saving
        fields = '__all__'
        extra_kwags = {
            'user': {'write_only': True}
        }

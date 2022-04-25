from rest_framework import serializers
from .models import Budget, Goal, Notifications, Saving


class GoalSerializers(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'collected': {'required': True},
            'title': {'unique': True}
        }


class SavingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Saving
        fields = '__all__'
        extra_kwags = {
            'user': {'write_only': True}
        }


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = '__all__'
        extra_kwags = {
            'user': {'write_only': True}
        }


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

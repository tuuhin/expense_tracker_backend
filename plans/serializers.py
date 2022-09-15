from rest_framework import serializers
from .models import Budget, Goal, Notifications, Reminder


class GoalSerializers(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'collected': {'required': True},

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

    def validate(self, data):
        if data['_from'] >= data['to']:
            raise serializers.ValidationError(
                'Start date must be prior to end date.')
        return data


class ReminderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reminder
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

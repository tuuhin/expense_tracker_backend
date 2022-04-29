from rest_framework import serializers
from .models import Expenses, Source, Category, Income
from django.contrib.auth.models import User


class SourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Source
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UpdateCategorySerializer(serializers.Serializer):
    source = serializers.CharField(max_length=50)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class IncomeSerializer(serializers.ModelSerializer):
    sources = SourceSerializer(many=True, read_only=True)

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }


class ExpenseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

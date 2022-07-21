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

    source = SourceSerializer(many=True, required=False)

    def create(self, validated_data):
        sources = validated_data.pop('source')
        income = Income.objects.create(**validated_data)
        for source in sources:
            source_object = Source.objects.filter(**source).first()
            if source_object:
                income.source.add(source_object.pk)
        return income

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'amount': {'required': True}
        }


class ExpenseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

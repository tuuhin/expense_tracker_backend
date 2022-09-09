from dataclasses import field
from rest_framework import serializers
from rest_framework.validators import ValidationError
from plans.models import Budget
from .models import Expenses, Source, Category, Income
from django.contrib.auth.models import User
from plans.serializers import BudgetSerializer


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

    # def create(self, validated_data):
    #     sources = validated_data.pop('source')
    #     income = Income.objects.create(**validated_data)
    #     for source in sources:
    #         source_object = Source.objects.filter(**source).first()
    #         if source_object:
    #             income.source.add(source_object.pk)
    #     return income

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'amount': {'required': True}
        }


class CreateIncomeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'amount': {'required': True}
        }


class ExpenseSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, required=False)
    budget = BudgetSerializer(many=False, read_only=False)

    # def create(self, validated_data):
    #     categories = validated_data.pop('categories')
    #     budget = validated_data.pop('budget')
    #     budget_object = Budget.objects.filter(**budget).first()

    #     expense = Expenses.objects.create(
    #         **validated_data, budget=budget_object)
    #     for category in categories:
    #         category_object = Category.objects.filter(**category).first()
    #         if category_object:
    #             expense.categories.add(category_object.pk)
    #     return expense

    # def validate(self, attrs):
    #     amount: float = attrs['amount']
    #     budget: Budget = Budget(**attrs['budget'])
    #     if budget.amount_used + amount > budget.total_amount:
    #         raise ValidationError(
    #             detail="This expense can't fit to this budget ")
    #     return super().validate(attrs)

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }


class CreateExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def validate(self, attrs):
        amount: float = attrs['amount']
        budget: Budget = attrs['budget']
        if budget.amount_used + amount > budget.total_amount:
            raise ValidationError(
                detail="This expense can't fit to this budget ")
        return super().validate(attrs)

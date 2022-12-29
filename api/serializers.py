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


class IncomeSerializer(serializers.ModelSerializer):

    source = SourceSerializer(many=True, required=False)

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'amount': {'required': False}
        }


class CreateIncomeSerializer(serializers.ModelSerializer):

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
    #     if budget.amount_left < amount:
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

        if budget.amount_left < amount:
            raise ValidationError(
                detail=f"This amount: {amount} is too large to  fit in  budget : {budget} ")
        return super().validate(attrs)


class UpdateExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def update(self, instance: Expenses, validated_data):
        old_amount: float = instance.amount
        old_budget: Budget = instance.budget
        amount: float = validated_data['amount']
        budget: Budget = validated_data['budget']

        if old_budget == budget:
            if budget.amount_left + old_amount < amount:
                print("here")
                raise ValidationError(
                    detail=f"This amount: {amount} is too large to  fit in  budget : {budget} ")
        else:
            if budget.amount_left < amount:
                print("now here")
                raise ValidationError(
                    detail=f"This amount: {amount} is too large to  fit in  budget : {budget} ")

        return super().update(instance, validated_data)


class EntriesSerializer(serializers.Serializer):
    highest_count = serializers.IntegerField()
    overall_count = serializers.IntegerField()
    previous = serializers.URLField(allow_blank=True)
    next = serializers.URLField(allow_blank=True)
    results = serializers.ListField(allow_empty=True)

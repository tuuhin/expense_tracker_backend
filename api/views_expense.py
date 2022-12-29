from typing import Optional

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import NotFound
from rest_framework.decorators import (
    api_view, permission_classes, parser_classes)

from .models import Expenses, Category
from .serializers import (
    ExpenseSerializer, CategorySerializer,
    CreateExpenseSerializer, UpdateExpenseSerializer)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def expenses(request: Request) -> Optional[Response]:
    if request.method == 'GET':
        expenses = Expenses.objects.filter(user=request.user)
        expense_serializer = ExpenseSerializer(
            expenses, many=True)
        return Response(expense_serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()
        data["user"] = request.user.pk
        # if request.data.get('categories'):
        #     categories = request.data.pop('categories')
        #     if categories:
        #         list_categories = []
        #         for category in categories:
        #             check_category = Category.objects.filter(
        #                 pk=category['id']).first()
        #             if check_category:

        #                 s_category = CategorySerializer(
        #                     check_category, many=False)

        #                 list_categories.append(
        #                     {'user': request.user.pk, **s_category.data})
        #     data['categories'] = list_categories
        # if request.data.get('budget'):
        #     budget = request.data.pop('budget')

        #     if budget:
        #         check_budget = Budget.objects.filter(pk=budget['id']).first()
        #         if check_budget:
        #             s_budget = BudgetSerializer(check_budget, many=False)
        #             user_budget = {'user': request.user.pk, **s_budget.data}
        #             data['budget'] = user_budget

        serialized_expense = CreateExpenseSerializer(data=data)

        if serialized_expense.is_valid():
            new_expense = serialized_expense.save()

            response = ExpenseSerializer(new_expense)

            return Response(response.data, status=status.HTTP_201_CREATED)

        return Response(serialized_expense.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upgrade_expense(request: Request, pk: int) -> Optional[Response]:
    user = request.user.pk

    if request.method == "PUT":
        data = request.data.copy()
        data['user'] = user
        expense = Expenses.objects.filter(user=user, pk=pk).first()

        if expense:
            serialized_expense = UpdateExpenseSerializer(expense, data=data)

            if serialized_expense.is_valid():
                updated_expense = serialized_expense.save()

                response = ExpenseSerializer(updated_expense, many=False)

                return Response(response.data, status=status.HTTP_202_ACCEPTED)

            return Response(serialized_expense.errors, status=status.HTTP_424_FAILED_DEPENDENCY)

        raise NotFound(f"ExpenseId: {pk} do not exists")

    if request.method == "DELETE":
        expense: Optional[Expenses] = Expenses.objects.filter(
            user=user, pk=pk).first()
        if expense:
            expense.delete()
            return Response({'data': f'Expense titled {expense.title} do not exits'}, status=status.HTTP_204_NO_CONTENT)
        raise NotFound('Could not remove this expense',
                       code=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def categories(request: Request) -> Response:

    if request.method == 'GET':
        categories = Category.objects.filter(user=request.user)
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        data = request.data.copy()
        data['user'] = request.user.pk
        serialized_category = CategorySerializer(data=data)

        if serialized_category.is_valid():
            serialized_category.save()
            return Response(serialized_category.data, status=status.HTTP_201_CREATED)
        return Response(serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def upgrade_categories(request: Request, pk: int) -> Optional[Response]:
    user = request.user.pk

    if request.method == 'PUT':
        data = {**request.data, "user": request.user.pk}

        category = Category.objects.get(pk=pk)

        if category:

            category_serializer = CategorySerializer(category, data=data)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response(category_serializer.data, status=status.HTTP_205_RESET_CONTENT)

            return Response(category_serializer.errors, status=status.HTTP_424_FAILED_DEPENDENCY)
        else:
            return Response({'message': 'source don\'t exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        category_exists = Category.objects.filter(user=user, pk=pk)

        if category_exists:
            category_exists.delete()
            return Response({'message': 'the source has been deleted '}, status=status.HTTP_204_NO_CONTENT)

        raise NotFound('source dont\'t exists', code=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Expenses, Category
from .serializers import ExpenseSerializer, CategorySerializer


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def expenses(request):

    if request.method == 'GET':
        expenses = Expenses.objects.filter(user=request.user)
        expense_serializer = ExpenseSerializer(expenses, many=True)
        return Response(expense_serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['user'] = request.user.pk
        serialized_expense = ExpenseSerializer(data=data)

        if serialized_expense.is_valid():
            serialized_expense.save()
            return Response(serialized_expense.data, status=status.HTTP_201_CREATED)

        return Response(serialized_expense.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET', 'POST'])
def categories(request):

    if request.method == 'GET':
        categories = Category.objects.filter(user=request.user)
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['user'] = request.user.pk
        serialized_category = CategorySerializer(data=data)

        if serialized_category.is_valid():
            return Response(serialized_category.data, status=status.HTTP_201_CREATED)
        return Response(serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def upgrade_categories(request, pk):
    user = request.user.pk

    if request.method == 'PUT':
        data = request.data
        data['user'] = user
        category = Category.objects.get(pk=pk)

        if category:

            category_serializer = CategorySerializer(category, data=data)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response(category_serializer.data, status=status.HTTP_205_RESET_CONTENT)

            return Response(category_serializer.errors, status=status.HTTP_424_FAILED_DEPENDENCY)
        else:
            return Response({'message': 'source don\'t exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELTE':
        category_exists = Category.objects.filter(user=user, pk=pk)

        if category_exists:
            category_exists.delete()
            return Response({'message': 'the source has been deleted '}, status=status.HTTP_204_NO_CONTENT)

        return Response({'message': 'source dont\'t exists'}, status=status.HTTP_404_NOT_FOUND)

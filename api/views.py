from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
from .models import Income, Expenses


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def base_information(request:Request) -> Response:
    user = request.user
    current_month = datetime.now().month

    total_income = sum([income for income in Income.objects.filter(user=user)])
    total_expense = sum([expense for expense in Expenses.objects.filter(user=user)])
    monthly_income = sum([income for income in Income.objects.filter(user=user) if income.added_at.month==current_month])
    monthly_expense = sum([expense for expense in Expenses.objects.filter(user=user) if expense.added_at.month==current_month])

    return Response({
        'total_income': total_income,
        'montly_income': monthly_income,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense
    }, status=status.HTTP_200_OK)

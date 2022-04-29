from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
from .models import Income, Expenses


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def base_information(request):
    user = request.user
    current_month = datetime.now().month
    total_income, total_expense = 0, 0
    monthly_income, monthly_expense = 0, 0

    for income in Income.objects.filter(user=user):
        total_income += income.amount
        if income.added_at.month == current_month:
            monthly_income += income.amount

    for expense in Expenses.objects.filter(user=user):
        total_expense += expense.amount
        if expense.added_at.month == current_month:
            monthly_expense += expense.amount

    return Response({
        'total_income': total_income,
        'montly_income': monthly_income,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense
    }, status=status.HTTP_200_OK)

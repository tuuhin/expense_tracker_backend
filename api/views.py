from django.utils import timezone
from django.db.models import Sum

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from .models import Income, Expenses


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def base_information(request: Request) -> Response:
    user = request.user
    current_month = timezone.now().month

    total_income = Income.objects.filter(
        user=user
    ).aggregate(Sum('amount')).get('amount__sum') or 0
    total_expense = Expenses.objects.filter(
        user=user
    ).aggregate(Sum('amount')).get('amount__sum') or 0
    monthly_income = Income.objects.filter(
        user=user,
        added_at__month=current_month
    ).aggregate(Sum('amount')).get('amount__sum') or 0
    monthly_expense = Expenses.objects.filter(
        user=user,
        added_at__month=current_month
    ).aggregate(Sum('amount')).get('amount__sum') or 0

    return Response({
        'total_income': total_income,
        'monthly_income': monthly_income,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense
    }, status=status.HTTP_200_OK)

from typing import Optional
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,  APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.http.request import QueryDict

from .models import Budget, Goal
from .serializers import BudgetSerializer, GoalSerializers


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def goals(request: Request) -> Optional[Response]:
    goals = Goal.objects.filter(user=request.user)
    serialized_goals = GoalSerializers(goals, many=True)
    return Response(serialized_goals.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def create_goal(request: Request) -> Response:
    data: QueryDict = request.data.copy()
    data['user'] = request.user.pk

    serialized_goals = GoalSerializers(data=data)
    if serialized_goals.is_valid():
        serialized_goals.save()
        return Response(serialized_goals.data, status=status.HTTP_201_CREATED)
    return Response(serialized_goals.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upgrade_goals(request: Request, pk: int) -> Response:

    if request.method == 'PUT':
        current_goal = Goal.objects.filter(pk=pk, user=request.user).first()
        data = request.data.copy()
        data["user"]= request.user.pk
        goal_serializer = GoalSerializers(current_goal, data=data)
        if goal_serializer.is_valid():
            goal_serializer.save()
            return Response(goal_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(goal_serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)

    if request.method == 'DELETE':
        current_goal = Goal.objects.filter(pk=pk, user=request.user).first()
        if current_goal:
            current_goal.delete()
            return Response({'detail': 'successfully removed'}, status=status.HTTP_204_NO_CONTENT)
        raise NotFound(detail="Goal don't extsts")


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def change_budget(request: Request, pk: int) -> Response:

    if request.method == 'PUT':
        current_budget: Budget = Budget.objects.filter(
            pk=pk, user=request.user).first()

        if current_budget.has_expired:
            raise APIException('An expired budget cannot be deleted',
                               code=status.HTTP_417_EXPECTATION_FAILED)

        data: dict = {**request.data, 'user': request.user.pk}

        if data.get('total_amount') <= sum([exp.amount for exp in current_budget.expenses_set.all()]):
            raise APIException('This amount is already is used in some expense ',
                               code=status.HTTP_424_FAILED_DEPENDENCY)

        budget_serializer = BudgetSerializer(current_budget, data=data)
        if budget_serializer.is_valid():
            budget_serializer.save()
            return Response(budget_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(budget_serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)

    # direct removal of budget are allowed if the expenses relation.length is zero

    if request.method == 'DELETE':
        budget_exists = Budget.objects.filter(pk=pk, user=request.user).first()

        if budget_exists:
            if budget_exists.expenses_set.count() == 0 or budget_exists.has_expired:

                budget_exists.delete()
                return Response({'detail': 'Budget has been deleted successfully'}, status=status.HTTP_202_ACCEPTED)

            raise APIException(
                'An un-expired budget cannot be removed remove all the expenses assocaited with it first', code=status.HTTP_406_NOT_ACCEPTABLE)

        raise NotFound(detail="Budget don't exists ",
                       code=status.HTTP_404_NOT_FOUND)


@ api_view(http_method_names=['GET', 'POST'])
@ permission_classes([IsAuthenticated])
def budget(request: Request) -> Response:

    if request.method == 'GET':
        budgets = Budget.objects.filter(user=request.user)
        budget_serializer = BudgetSerializer(budgets, many=True)
        return Response(budget_serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.pk

        serialized_budget = BudgetSerializer(data=data)

        if serialized_budget.is_valid():
            serialized_budget.save()
            return Response(serialized_budget.data, status=status.HTTP_201_CREATED)
        return Response(serialized_budget.errors, status=status.HTTP_424_FAILED_DEPENDENCY)


# @api_view(http_method_names=['GET'])
# @permission_classes([IsAuthenticated])
# def show_notifications(request):

#     notifications = Notifications.objects.filter(user=request.user)
#     serializer = NotificationSerializer(notifications, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

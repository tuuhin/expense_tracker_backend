from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Budget, Goal, Reminder
from .serializers import BudgetSerializer, GoalSerializers


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def goals(request: Request) -> Response:

    if request.method == 'GET':
        goals = Goal.objects.filter(user=request.user)
        serialized_goals = GoalSerializers(goals, many=True)
        return Response(serialized_goals.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.pk
        serialized_goals = GoalSerializers(data=data)
        if serialized_goals.is_valid():
            return Response(serialized_goals.data, status=status.HTTP_201_CREATED)
        return Response(serialized_goals.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def upgrade_goals(request: Request, pk: int) -> Response:

    if request.method == 'PUT':
        current_goal = Goal.objects.filter(pk=pk, user=request.user).first()
        data = request.data.copy()
        data['user'] = request.user.pk
        goal_serializer = GoalSerializers(current_goal, data=data)
        if goal_serializer.is_valid():
            return Response(goal_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(goal_serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)

    if request.method == 'DELETE':
        current_goal = Goal.objects.filter(pk=pk, user=request.user).first()
        if current_goal:
            current_goal.delete()
            return Response({'message': 'successfully removed'}, status=status.HTTP_204_NO_CONTENT)
        raise NotFound(detail="Goal don't extsts")


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def remove_budget(request: Request, pk: int) -> Response:

    if request.method == 'PUT':
        current_budget = Budget.objects.filter(
            pk=pk, user=request.user).first()
        if current_budget.has_expired:
            return Response({'detail': 'An expired budget cannot be deleted '}, status=status.HTTP_417_EXPECTATION_FAILED)

        data = request.data.copy()
        data['user'] = request.user.pk
        budget_serializer = BudgetSerializer(current_budget, data=data)
        if budget_serializer.is_valid():
            return Response(budget_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(budget_serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)

    # direct removal of budget are allowed if the expenses relation.length is zero

    if request.method == 'DELETE':
        budget_exists = Budget.objects.filter(pk=pk).first()

        if budget_exists:
            if budget_exists.expenses_set.count() == 0:
                budget_exists.delete()
                return Response({'detail': 'Budget has been deleted successfully'}, status=status.HTTP_202_ACCEPTED)

            if budget_exists.has_expired:
                budget_exists.delete()
                return Response({'detail': 'Budget has been deleted successfully'}, status=status.HTTP_202_ACCEPTED)

            raise NotFound(
                'An un-expired budget cannot be removed remove all the expenses assocaited with it first', code=status.HTTP_406_NOT_ACCEPTABLE)

        raise NotFound(detail="Budget don't exists ",
                       code=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
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

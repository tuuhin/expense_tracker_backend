from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import BudgetSerializer, GoalSerializers, NotificationSerializer
from .models import Budget, Goal, Notifications


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def goals(request):

    if request.method == 'GET':
        goals = Goal.objects.filter(user=request.user)
        serialized_goals = GoalSerializers(goals, many=True)
        return Response(serialized_goals.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.pk
        goal = GoalSerializers(data=data)
        if goal.is_valid():
            return Response(goal.data, status=status.HTTP_201_CREATED)
        return Response(goal.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def upgrade_goals(request, pk):

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
        return Response({'message': 'failed to get the goals'}, status=status.HTTP_424_FAILED_DEPENDENCY)


@api_view(http_method_names=['DELETE'])
@permission_classes([IsAuthenticated])
def remove_budget(request, pk):

    if request.method == 'DELETE':
        budget_exists = Budget.objects.filter(pk=pk).first()

        if budget_exists:
            budget_exists.delete()
            return Response({'message': 'Budget has been deleted successfully'}, status=status.HTTP_302_FOUND)

        return Response({'messsage': 'failed to get the user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def budget(request):

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

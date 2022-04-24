from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import GoalSerializers
from .models import Goal


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

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
        data['user'] = request.user
        goal = GoalSerializers(data=data)
        if goal.is_valid():
            return Response(goal.data, status=status.HTTP_201_CREATED)
        return Response(goal.errors, status=status.HTTP_400_BAD_REQUEST)

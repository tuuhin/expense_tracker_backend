from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer
from .models import Notifications


class NotificationPagination(LimitOffsetPagination):
    default_limit: int = 10
    max_limit: int = 20
    offset_query_param: str = "offset"


class NotificationView(ListAPIView):
    queryset = Notifications.objects.all()
    pagination_class = NotificationPagination
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user.pk)
        return super().get(request, *args, **kwargs)

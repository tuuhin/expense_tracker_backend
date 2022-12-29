from rest_framework.permissions import IsAuthenticated
from drf_multiple_model.views import FlatMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination

from .serializers import ExpenseSerializer, IncomeSerializer, EntriesSerializer
from .models import Expenses, Income


class EntriesPagination(MultipleModelLimitOffsetPagination):
    default_limit = 6


class Entries(FlatMultipleModelAPIView):

    sorting_fields = '-added_at',
    pagination_class = EntriesPagination
    permission_classes = [IsAuthenticated]
    serializer_class = EntriesSerializer

    def get_querylist(self):
        querylist = [
            {
                'queryset': Income.objects.filter(user=self.request.user.pk),
                'serializer_class': IncomeSerializer,
                'label': 'income',
            },
            {
                'queryset': Expenses.objects.filter(user=self.request.user.pk),
                'serializer_class': ExpenseSerializer,
                'label': 'expense'
            },
        ]
        return querylist

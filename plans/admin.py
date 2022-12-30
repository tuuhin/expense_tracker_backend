from django.contrib import admin
from .models import Budget, Goal,  Notifications
# Register your models here.


@admin.register(Goal)
class GoalsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'collected', 'is_accomplished')
    ordering = '-updated_at',
    list_filter = 'user',


@admin.register(Notifications)
class NotificationManager(admin.ModelAdmin):

    list_display = 'id', 'title', 'user', 'at', 'status',
    search_fields = 'user__username',
    list_filter = 'user', 'status', 'signal'
    ordering = 'at',
    # actions_on_top = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'budget_start', 'budget_end',
                    'total_amount', 'amount_used', 'amount_left', 'has_expired',)
    ordering = '-updated',
    list_filter = 'user',

    @admin.display(description='Start')
    def budget_start(self, obj: Budget):
        return obj._from.strftime('%Y-%m-%d')

    @admin.display(description="End")
    def budget_end(self, obj: Budget):
        return obj.to.strftime("%Y-%m-%d")

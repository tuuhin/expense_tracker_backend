from django.contrib import admin
from .models import Budget, Goal,  Notifications, Reminder
# Register your models here.


@admin.register(Goal)
class GoalsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'collected', 'is_accomplished')
    ordering = '-updated_at',
    list_filter = 'user',


@admin.register(Notifications)
class NotificationManager(admin.ModelAdmin):
    list_display = ('title', 'user', 'at', 'status')
    search_fields = ('user__username',)
    list_filter = ('user', 'status')
    actions_on_top = False


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', '_from', 'to',
                    'total_amount', 'amount_used', 'has_expired')
    ordering = '-issued_at',
    list_filter = 'user',

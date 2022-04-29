from django.contrib import admin
from .models import Goal, Saving, Budget, Notifications
# Register your models here.

admin.site.register(Saving)
admin.site.register(Budget)


@admin.register(Goal)
class GoalsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'collected', 'is_accomplished')
    ordering = ('-updated_at',)
    list_filter = ('user', 'is_accomplished')


@admin.register(Notifications)
class NotificationManager(admin.ModelAdmin):
    list_display = ('title', 'user', 'at')
    list_filter = ('user',)

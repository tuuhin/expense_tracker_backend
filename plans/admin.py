from django.contrib import admin
from .models import Goal, Saving, Budget, Notifications
# Register your models here.
admin.site.register(Goal)
admin.site.register(Saving)
admin.site.register(Budget)
admin.site.register(Notifications)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),
    # authentication routes
    path('auth/', include('base.urls')),
    # api routes
    path('api/', include('api.urls')),
    # plans route
    path('plans/', include('plans.urls'))
]

admin.site.site_header = "Expense Tracker Backend"

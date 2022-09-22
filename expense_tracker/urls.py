from django.contrib import admin
from django.urls import path, include
from .swagger import schema_view


urlpatterns = [
    # swagger
    path('swagger', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
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

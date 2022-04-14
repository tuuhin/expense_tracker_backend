from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # django admin
    path('admin/', admin.site.urls),
    # authentication routes
    path('auth/', include('base.urls')),
    # api routes
    path('api/', include('api.urls'))

]

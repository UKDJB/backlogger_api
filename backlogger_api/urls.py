# backlogger_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentications.urls')),
    path('api/organisations/', include('organisations.urls')),
    path('api/items/', include('items.urls')),
]

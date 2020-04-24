from django.contrib import admin
from django.urls import path, include
from .views import Home
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', include(notifications.urls, namespace='notifications')),
    path('avatar/', include('avatar.urls')),

    path('api/', include('users.urls')),
    path('api/rides/', include('rides.urls')),
    path('', Home.as_view(), name='home'),
]

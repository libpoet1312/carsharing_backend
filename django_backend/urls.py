from django.contrib import admin
from django.urls import path, include
from .views import Home
import notifications.urls
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),  # Back-End Admin Page
    path('notifications/', login_required(include(notifications.urls, namespace='notifications'))),  #
    path("schema/", Schema.as_view()),

    path('notifier/', include('notifier.urls')),

    path('api/', include('rides.urls')),  # the real api endpoint
    path('cars/', include('cars.urls')),

    path('', include('users.urls')),
    path('', Home.as_view(), name='home'),  # test template home view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # serving locally profile images

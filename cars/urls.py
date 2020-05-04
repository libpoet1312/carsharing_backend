from .views import *
from rest_framework import routers

urlpatterns = []

router = routers.SimpleRouter()
router.register(r'car', CarViewSet)
urlpatterns += router.urls

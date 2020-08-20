from django.urls import path, include
from .views import *


urlpatterns = [
    path('', RideListView.as_view(), name='list_rides'),
    path('myrides/', MyRidesListView.as_view(), name='myrides'),
    path('create/', RideCreateView.as_view(), name='create_ride'),
    path('<int:pk>/', RideDetailView.as_view(), name='detail_ride'),
    path('<int:pk>/edit/', RideEditView.as_view(), name='edit_ride'),
    path('', include('rideRequests.urls')),
]

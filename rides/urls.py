from django.urls import path
from .views import *

urlpatterns = [
    path('', RideListView.as_view(), name='list_rides'),
    path('create/', RideCreateView.as_view(), name='create_ride'),
    path('<int:pk>/', RideDetailView.as_view(), name='detail_ride'),
    path('<int:pk>/edit/', RideEditView.as_view(), name='edit_ride'),

    path('<int:pk>/getrequests/', getjoinRequests.as_view(), name='get_join_requests'),

    path('<int:pk>/acceptjoin/<int:userid>/', acceptJoin.as_view(), name='accept_join'),
    path('<int:pk>/declinejoin/<int:userid>/', declineJoin.as_view(), name='decline_join'),

    path('<int:pk>/join/', joinRequest.as_view(), name='join_ride'),
    path('<int:pk>/canceljoin/', canceljoinRequest.as_view(), name='cancel_join_request'),

    path('<int:pk>/unjoin/', unJoin.as_view(), name='unjoin_ride'),  # from user scope
    path('<int:pk>/kick/<int:userid>/', kick.as_view(), name='kick'),  # from driver scope
]

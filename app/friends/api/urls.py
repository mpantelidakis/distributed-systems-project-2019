from django.urls import path

from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    # FriendRequestListAPIView,
    # FriendRequestCreateAPIView,
    # FriendRequestDeleteAPIView,
)

app_name = 'friends'

urlpatterns = [
    path('profiles/',ProfileListAPIView.as_view(), name='profile-list'),
    path('profiles/<slug>/',ProfileDetailAPIView.as_view(), name='profile-detail'),
    # path('friend_requests/',FriendRequestListAPIView.as_view(), name='friend_request-list'),
    # path('friend_requests/create/',FriendRequestCreateAPIView.as_view(), name='friend_request-create'),
    # path('friend_requests/<pk>/delete/',FriendRequestDeleteAPIView.as_view(), name='friend_request-delete'),
]

from django.urls import path

from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView
)

urlpatterns = [
    path('profiles/',ProfileListAPIView.as_view(), name='list'),
    path('profiles/<slug>/',ProfileDetailAPIView.as_view(), name='detail'),
]

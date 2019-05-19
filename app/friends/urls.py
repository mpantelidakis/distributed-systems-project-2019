from django.conf.urls import url
from django.urls import path

from .views import (
	ProfileDetailView,
	ManageFriendsTemplateViewView,
	)

app_name='friends'

urlpatterns = [
    path('', ManageFriendsTemplateViewView.as_view(), name='manage'),
    path('<slug>/', ProfileDetailView.view_profile),
]


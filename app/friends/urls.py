from django.conf.urls import url
from django.urls import path

from .views import (
	UserDisplay, 
	ProfileView,
	ProfileTemplateView,
	)

app_name='friends'

urlpatterns = [
    path('me/', ProfileTemplateView.as_view(), name='me'),
    path('<slug>/', ProfileView.as_view()),
]


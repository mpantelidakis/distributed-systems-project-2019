from django.conf.urls import url
from django.urls import path

from django.contrib.auth import views as auth_views

from .views import (
	UserDisplay, 
	ProfileView, 
	)

urlpatterns = [
    url(r'^$', UserDisplay.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', ProfileView.as_view()),
]
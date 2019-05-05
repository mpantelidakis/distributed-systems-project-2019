from django.conf.urls import url

from .views import (
	UserDisplay, 
	ProfileView, 
	FriendRequestView, 
	cancel_friend_request,
	accept_friend_request,
	delete_friend_request
	)

urlpatterns = [
    url(r'^$', UserDisplay.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', ProfileView.as_view()),
    url(r'^friend-request/send/(?P<id>[\w-]+)/$', FriendRequestView.send_friend_request),
    url(r'^friend-request/cancel/(?P<id>[\w-]+)/$', cancel_friend_request),
    url(r'^friend-request/accept/(?P<id>[\w-]+)/$', accept_friend_request),
    url(r'^friend-request/delete/(?P<id>[\w-]+)/$', delete_friend_request),
]
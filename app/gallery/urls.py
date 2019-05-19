from django.conf.urls import url
from django.urls import path

from .views import (
	GalleryListTemplateView,
    GallreyDetailView,
	)

app_name='gallery'

urlpatterns = [
    path('', GalleryListTemplateView.as_view(), name='list'),
    path('<pk>/', GallreyDetailView.view_gallery, name='detail'),
    # path('<slug>/', ProfileView.as_view()),
]
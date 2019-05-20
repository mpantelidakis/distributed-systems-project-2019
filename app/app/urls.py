"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from .views import HomeTemplateView, TestAuthView, LogoutViewEx
from rest_auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.api.urls', namespace='user-api')),
    path('api/gallery/', include('gallery.api.urls', namespace='gallery-api')),
    path('api/friends/', include('friends.api.urls', namespace='friends-api')),
    path('api/comment/', include('comment.urls')),
    path('friends/', include('friends.urls', namespace='friends')),
    path('galleries/', include('gallery.urls', namespace='gallery')),
    path('rest-auth/logout/', LogoutViewEx.as_view(), name='rest_logout'),
    path('rest-auth/login/', LoginView.as_view(), name='rest_login'),
    
    
    path('', HomeTemplateView.as_view(), name='home', ),
    path('test_auth/', TestAuthView.as_view(), name='test_auth', ),
    

    # add url for our media files
    # by default the django devenlopment server
    # does NOT serve media files

    # Makes the media url available in the devserver
    # so that we can test without having to set up
    # a separate webserver for serving these media files
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]

# if bool(settings.DEBUG):
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
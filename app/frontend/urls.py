from django.urls import path
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('',views.HomePageView),
    # path('^signup/$',views.signup_view),
    # path('^login/$',views.login_view),
]

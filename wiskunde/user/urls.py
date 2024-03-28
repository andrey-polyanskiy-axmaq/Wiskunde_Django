from django.urls import path, include
from . import views
from django.urls import re_path

urlpatterns = [
   path('', views.index, name='userinfo'),
   re_path(r'^login/$', views.user_login, name='login')
]





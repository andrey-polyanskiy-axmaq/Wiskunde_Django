from django.urls import path, include
from . import views
from django.urls import re_path

urlpatterns = [
   path('', include(('main.urls', 'main'), namespace='main')),
   path('profile', views.index, name='userinfo'),
   re_path(r'^login/$', views.user_login, name='login'),
   path('logoutuser/', views.logout_user, name='logout')
]





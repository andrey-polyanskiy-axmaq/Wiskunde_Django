from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('', views.index, name='home'),
   path('info.html', views.info, name='info'),
   path('contacts.html', views.contacts, name='contact')
]





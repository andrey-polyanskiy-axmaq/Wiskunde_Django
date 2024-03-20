from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.index, name='home'),
   path('info.html', views.info, name='info'),
   path('contacts.html', views.contacts, name='contact')
]





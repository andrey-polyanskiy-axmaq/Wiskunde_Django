from django.urls import path, include
from . import views
from django.urls import re_path

urlpatterns = [
    path('homepage', include(('main.urls', 'main'), namespace='main')),
    path('', views.index, name='userinfo'),
    re_path(r'^login/$', views.user_login, name='login'),
    path('logoutuser/', views.logout_user, name='logout'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('lessons/', views.lessons, name='lessonsuser'),
    path('lesson-files/<str:filename>/', views.download_lesson_PDF_file, name='download_lesson_file_user'),
    path('upload-feedback/', views.upload_feedback, name='upload_feedback'),
    path('schedule/', views.schedule, name='schedule'),
]

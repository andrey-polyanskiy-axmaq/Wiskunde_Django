from django.contrib import admin
from django.urls import path, include
from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    re_path(r'^user/', include('user.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

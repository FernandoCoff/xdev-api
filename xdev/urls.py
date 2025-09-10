from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.urls import re_path
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('post/', include('posts.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))

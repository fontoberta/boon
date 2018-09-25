from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.conf.urls import url, include
from content import urls as content_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^oauth/',
        include('oauth2_provider.urls', namespace='oauth2_provider'))
]

urlpatterns += content_urls.urlpatterns_content

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

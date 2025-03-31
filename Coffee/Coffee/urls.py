from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


handler404 = 'mvt.errors.not_found_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mvt.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

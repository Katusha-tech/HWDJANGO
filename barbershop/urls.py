from django.contrib import admin
from django.urls import path
from core.views import landing
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    # Подключаем маршруты из приложения core
    path('barbershop/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
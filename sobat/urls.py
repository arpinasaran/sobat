from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('review/', include('review.urls')),
    path('product/', include('product.urls')),
    path('shop/', include('shop.urls')),
    path('', include('authentication.urls')),
    path('', include('main.urls')),
    path('', include('forum.urls')),
    path('resep/', include('resep.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

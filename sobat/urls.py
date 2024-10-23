from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('shop/', include('shop.urls')),
    path('', include('authentication.urls')),
    path('', include('main.urls')),
    path('forum/', include('forum.urls')),
]

from django.contrib import admin
from django.urls import path,include
from daftar_favorit import views
app_name = 'daftar_favorite'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favorite/', include('daftar_favorit.urls')),
    path('review/', include('review.urls')),
    path('product/', include('product.urls')),
    path('shop/', include('shop.urls')),
    path('', include('authentication.urls')),
    path('', include('main.urls')),
    path('forum/', include('forum.urls')),
    path('resep/', include('resep.urls'))
]

from django.urls import path
from authentication.views import register, login_user, logout_user, login_mobile, register_mobile, logout_mobile

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('login_mobile/', login_mobile, name='login_mobile'),
    path('register_mobile/', register_mobile, name='register_mobile'),
    path('logout_mobile/', logout_mobile, name='logout_mobile'),
]
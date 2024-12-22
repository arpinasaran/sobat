from django.urls import path
from authentication import views
from authentication.views import register, login_user, logout_user
from authentication.views import register_mobile, login_mobile, logout_mobile, get_user_role

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register_mobile/', register_mobile, name='register_mobile'),
    path('login_mobile/', login_mobile, name='login_mobile'),
    path('logout_mobile/', logout_mobile, name='logout_mobile'),
    path('get_user_role/', get_user_role, name='get_user_role'),
]
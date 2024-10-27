from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User


class CreateUserForm(UserCreationForm):
    usable_password = None
    class Meta:
        model = User
        fields = ["nama", "username", "password1", "password2", "role"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = []
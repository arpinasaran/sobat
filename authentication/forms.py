from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User


class CreateUserForm(UserCreationForm):
    usable_password = None
    class Meta:
        model = User
        fields = ["nama", "username", "password1", "password2", "role"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full border border-gray-300 rounded-md p-1 focus:outline-none focus:ring-2 focus:ring-[#254922] focus:border-transparent'
            })
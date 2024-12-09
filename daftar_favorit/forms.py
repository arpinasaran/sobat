from django.forms import ModelForm
from daftar_favorit.models import Favorite


class FavoriteForm(ModelForm):
    class Meta:
        model = Favorite
        fields = ["catatan"]
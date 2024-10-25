from django.db import models
from authentication.models import User
# from produk.models import Produk
# from toko.models import Toko
# from resep.models import Resep

# Create your models here.
class Pertanyaan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # produk_tanya = models.ForeignKey(Produk, on_delete=models.CASCADE)
    # toko_tanya = models.ForeignKey(Toko, on_delete=models.CASCADE)
    # resep_tanya = models.ForeignKey(Resep, on_delete=models.CASCADE)
    pertanyaan = models.TextField()
    terjawab = models.BooleanField(default=False)

class Jawaban(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.OneToOneField(Pertanyaan, on_delete=models.CASCADE)
    jawaban = models.TextField()
    # produk_jawab = models.ForeignKey(Produk, on_delete=models.CASCADE)
    # toko_jawab = models.ForeignKey(Toko, on_delete=models.CASCADE)
    # resep_jawab = models.ForeignKey(Resep, on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLES = [
        ("pengguna", "Pengguna"),
        ("apoteker", "Apoteker"),
    ]

    nama = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.nama
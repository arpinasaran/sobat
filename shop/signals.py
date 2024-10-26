# shop/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import time

User = get_user_model()

@receiver(post_migrate)
def create_default_shops(sender, **kwargs):
    if sender.name == 'shop':  # Only run for shop app
        create_sample_shops()

def create_sample_shops():
    from .models import ShopProfile  # Import here to avoid circular import

    sample_shops = [
        {
            "username": "apotek_sehat",
            "email": "apotek_sehat@example.com",
            "shop_name": "Apotek Sehat Sejahtera",
            "address": "Jl. Merdeka No. 123, Jakarta Pusat",
            "opening_time": time(8, 0),
            "closing_time": time(21, 0)
        },
        {
            "username": "medika_plus",
            "email": "medika_plus@example.com",
            "shop_name": "Medika Plus Pharmacy",
            "address": "Jl. Sudirman No. 45, Jakarta Selatan",
            "opening_time": time(7, 0),
            "closing_time": time(22, 0)
        },
        {
            "username": "farma_care",
            "email": "farma_care@example.com",
            "shop_name": "FarmaCare Center",
            "address": "Jl. Gatot Subroto No. 67, Jakarta Selatan",
            "opening_time": time(8, 30),
            "closing_time": time(20, 30)
        },
        {
            "username": "sehat_express",
            "email": "sehat_express@example.com",
            "shop_name": "Sehat Express Pharmacy",
            "address": "Jl. Asia Afrika No. 89, Bandung",
            "opening_time": time(7, 30),
            "closing_time": time(21, 30)
        },
        {
            "username": "apotek_familia",
            "email": "apotek_familia@example.com",
            "shop_name": "Apotek Familia",
            "address": "Jl. Diponegoro No. 156, Surabaya",
            "opening_time": time(8, 0),
            "closing_time": time(20, 0)
        },
        {
            "username": "medika_mart",
            "email": "medika_mart@example.com",
            "shop_name": "Medika Mart",
            "address": "Jl. Pahlawan No. 234, Semarang",
            "opening_time": time(7, 0),
            "closing_time": time(21, 0)
        },
        {
            "username": "healthcare_one",
            "email": "healthcare_one@example.com",
            "shop_name": "Healthcare One",
            "address": "Jl. Ahmad Yani No. 78, Medan",
            "opening_time": time(8, 0),
            "closing_time": time(22, 0)
        },
        {
            "username": "apotek_prima",
            "email": "apotek_prima@example.com",
            "shop_name": "Apotek Prima Sehat",
            "address": "Jl. Veteran No. 90, Yogyakarta",
            "opening_time": time(7, 30),
            "closing_time": time(20, 30)
        },
        {
            "username": "farma_plus",
            "email": "farma_plus@example.com",
            "shop_name": "Farma Plus",
            "address": "Jl. Imam Bonjol No. 112, Denpasar",
            "opening_time": time(8, 0),
            "closing_time": time(21, 0)
        },
        {
            "username": "sehat_bersama",
            "email": "sehat_bersama@example.com",
            "shop_name": "Sehat Bersama Pharmacy",
            "address": "Jl. Pemuda No. 145, Makassar",
            "opening_time": time(7, 0),
            "closing_time": time(22, 0)
        }
    ]

    with transaction.atomic():
        for shop_data in sample_shops:
            # Create user if doesn't exist
            user, _ = User.objects.get_or_create(
                username=shop_data["username"],
                defaults={
                    'email': shop_data["email"],
                    'password': 'defaultpassword123',
                    'role': 'apoteker'  # Assuming you have this field
                }
            )
            
            # Create shop if doesn't exist
            ShopProfile.objects.get_or_create(
                owner=user,
                defaults={
                    'name': shop_data["shop_name"],
                    'address': shop_data["address"],
                    'opening_time': shop_data["opening_time"],
                    'closing_time': shop_data["closing_time"]
                }
            )
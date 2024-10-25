from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from datetime import datetime, time
from shop.models import ShopProfile

User = get_user_model()

sample_shops = [
    {
        "username": "apotek_sehat",
        "shop_name": "Apotek Sehat Sejahtera",
        "address": "Jl. Merdeka No. 123, Jakarta Pusat",
        "opening_time": time(8, 0),
        "closing_time": time(21, 0)
    },
    {
        "username": "medika_plus",
        "shop_name": "Medika Plus Pharmacy",
        "address": "Jl. Sudirman No. 45, Jakarta Selatan",
        "opening_time": time(7, 0),
        "closing_time": time(22, 0)
    },
    {
        "username": "farma_care",
        "shop_name": "FarmaCare Center",
        "address": "Jl. Gatot Subroto No. 67, Jakarta Selatan",
        "opening_time": time(8, 30),
        "closing_time": time(20, 30)
    },
    {
        "username": "sehat_express",
        "shop_name": "Sehat Express Pharmacy",
        "address": "Jl. Asia Afrika No. 89, Bandung",
        "opening_time": time(7, 30),
        "closing_time": time(21, 30)
    },
    {
        "username": "apotek_familia",
        "shop_name": "Apotek Familia",
        "address": "Jl. Diponegoro No. 156, Surabaya",
        "opening_time": time(8, 0),
        "closing_time": time(20, 0)
    },
    {
        "username": "medika_mart",
        "shop_name": "Medika Mart",
        "address": "Jl. Pahlawan No. 234, Semarang",
        "opening_time": time(7, 0),
        "closing_time": time(21, 0)
    },
    {
        "username": "healthcare_one",
        "shop_name": "Healthcare One",
        "address": "Jl. Ahmad Yani No. 78, Medan",
        "opening_time": time(8, 0),
        "closing_time": time(22, 0)
    },
    {
        "username": "apotek_prima",
        "shop_name": "Apotek Prima Sehat",
        "address": "Jl. Veteran No. 90, Yogyakarta",
        "opening_time": time(7, 30),
        "closing_time": time(20, 30)
    },
    {
        "username": "farma_plus",
        "shop_name": "Farma Plus",
        "address": "Jl. Imam Bonjol No. 112, Denpasar",
        "opening_time": time(8, 0),
        "closing_time": time(21, 0)
    },
    {
        "username": "sehat_bersama",
        "shop_name": "Sehat Bersama Pharmacy",
        "address": "Jl. Pemuda No. 145, Makassar",
        "opening_time": time(7, 0),
        "closing_time": time(22, 0)
    }
]

def create_sample_shops():
    for shop_data in sample_shops:
        # Create user if doesn't exist
        user, created = User.objects.get_or_create(
            username=shop_data["username"],
            defaults={'password': 'defaultpassword123'}
        )
        
        # Create shop if doesn't exist
        shop, created = ShopProfile.objects.get_or_create(
            owner=user,
            defaults={
                'name': shop_data["shop_name"],
                'address': shop_data["address"],
                'opening_time': shop_data["opening_time"],
                'closing_time': shop_data["closing_time"]
            }
        )
        
        if created:
            print(f"Created shop: {shop.name}")
        else:
            print(f"Shop already exists: {shop.name}")

# Run this function in Django shell to create the sample shops
# python manage.py shell
# from shop.sample_data import create_sample_shops
# create_sample_shops()
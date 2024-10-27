from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import ShopProfile, ShopProduct
from product.models import DrugEntry
from datetime import time
import uuid

User = get_user_model()

class ShopModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='apoteker'
        )
        
        # Create test shop
        cls.shop = ShopProfile.objects.create(
            owner=cls.user,
            name='Test Shop',
            address='Test Address',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )
        
        # Create test drug
        cls.drug = DrugEntry.objects.create(
            name='Test Drug',
            description='Test Description',
            category='Test Category',
            selling_unit='strip',
            composition='Test Composition',
            manufacturer='Test Manufacturer',
            drug_form='tablet'
        )

    def test_shop_str_representation(self):
        self.assertEqual(str(self.shop), f"Test Shop - {self.user.username}")

    def test_shop_product_creation(self):
        shop_product = ShopProduct.objects.create(
            shop=self.shop,
            product=self.drug,
            stock=10,
            selling_price=100000.00
        )
        self.assertEqual(shop_product.stock, 10)
        self.assertEqual(str(shop_product), f"Test Drug at Test Shop")

class ShopViewTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='apoteker'
        )
        
        # Create test shop
        self.shop = ShopProfile.objects.create(
            owner=self.user,
            name='Test Shop',
            address='Test Address',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )
        
        # Create test drug
        self.drug = DrugEntry.objects.create(
            name='Test Drug',
            description='Test Description',
            category='Test Category',
            selling_unit='strip',
            composition='Test Composition',
            manufacturer='Test Manufacturer',
            drug_form='tablet'
        )
        
        self.client = Client()

    def test_shop_list_view(self):
        response = self.client.get(reverse('shop:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop_list.html')

    def test_shop_profile_view(self):
        response = self.client.get(reverse('shop:profile', kwargs={'shop_id': self.shop.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/profile.html')

    def test_create_shop_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('shop:create_shop'))
        self.assertEqual(response.status_code, 200)
        
        shop_data = {
            'name': 'New Test Shop',
            'address': 'New Test Address',
            'opening_time': '09:00',
            'closing_time': '17:00'
        }
        response = self.client.post(reverse('shop:create_shop'), shop_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ShopProfile.objects.filter(name='New Test Shop').exists())

    def test_create_shop_unauthenticated(self):
        response = self.client.get(reverse('shop:create_shop'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_manage_products(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request
        response = self.client.get(reverse('shop:manage_products', kwargs={'shop_id': self.shop.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/manage_products.html')
        
        # Test POST request
        response = self.client.post(
            reverse('shop:manage_products', kwargs={'shop_id': self.shop.id}),
            {'selected_products': [str(self.drug.id)]}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ShopProduct.objects.filter(shop=self.shop, product=self.drug).exists())

    def test_edit_profile(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request
        response = self.client.get(reverse('shop:edit_profile', kwargs={'shop_id': self.shop.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/edit_profile.html')
        
        # Test POST request
        updated_data = {
            'name': 'Updated Shop',
            'address': 'Updated Address',
            'opening_time': '10:00',
            'closing_time': '18:00'
        }
        response = self.client.post(
            reverse('shop:edit_profile', kwargs={'shop_id': self.shop.id}),
            updated_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.name, 'Updated Shop')

    def test_delete_shop(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request (confirmation page)
        response = self.client.get(reverse('shop:delete_shop', kwargs={'shop_id': self.shop.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/delete_shop.html')
        
        # Test POST request (actual deletion)
        response = self.client.post(reverse('shop:delete_shop', kwargs={'shop_id': self.shop.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(ShopProfile.objects.filter(id=self.shop.id).exists())

class ShopCatalogTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='apoteker'
        )
        
        # Create test shop
        self.shop = ShopProfile.objects.create(
            owner=self.user,
            name='Test Shop',
            address='Test Address',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )
        
        # Create test drugs
        self.drug1 = DrugEntry.objects.create(
            name='Test Drug 1',
            description='Test Description 1',
            category='Category A',
            selling_unit='strip',
            composition='Test Composition 1',
            manufacturer='Test Manufacturer',
            drug_form='tablet'
        )
        
        self.drug2 = DrugEntry.objects.create(
            name='Test Drug 2',
            description='Test Description 2',
            category='Category B',
            selling_unit='strip',
            composition='Test Composition 2',
            manufacturer='Test Manufacturer',
            drug_form='tablet'
        )
        
        # Create shop products
        ShopProduct.objects.create(shop=self.shop, product=self.drug1)
        ShopProduct.objects.create(shop=self.shop, product=self.drug2)

    def test_catalog_view(self):
        response = self.client.get(reverse('shop:catalog', kwargs={'shop_id': self.shop.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/catalog.html')

    def test_catalog_category_filter(self):
        response = self.client.get(
            reverse('shop:catalog_category', 
                   kwargs={'shop_id': self.shop.id, 'category': 'Category A'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/catalog.html')
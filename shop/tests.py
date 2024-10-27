from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import ShopProfile, ShopProduct
from product.models import DrugEntry
import uuid
from decimal import Decimal
from datetime import time
import json

from django.contrib.admin.sites import AdminSite
from .admin import ShopProfileAdmin

from shop.forms import ShopProfileForm

User = get_user_model()

class ShopProfileFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'New Shop',
            'address': '123 New St',
            'opening_time': time(9, 0),
            'closing_time': time(17, 0),
        }
        form = ShopProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form_missing_name(self):
        form_data = {
            'address': '123 New St',
            'opening_time': time(9, 0),
            'closing_time': time(17, 0),
        }
        form = ShopProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class ShopProfileAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='testpass123',
            role='admin'
        )
        self.shop = ShopProfile.objects.create(
            owner=self.user,
            name='Admin Test Shop',
            address='123 Admin Street',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )
        self.shop_admin = ShopProfileAdmin(ShopProfile, self.admin_site)

    def test_admin_display(self):
        """Test the custom admin display for ShopProfile"""
        self.assertIn('name', self.shop_admin.list_display)
        self.assertIn('owner', self.shop_admin.list_display)

class ShopProfileModelTest(TestCase):
    def setUp(self):
        # Create a test user with the apoteker role
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.role = 'apoteker'  # Set role after creation
        self.user.save()

        # Create a test shop
        self.shop = ShopProfile.objects.create(
            owner=self.user,
            name='Test Shop',
            address='123 Test Street',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )

    def test_shop_creation(self):
        self.assertTrue(isinstance(self.shop, ShopProfile))
        self.assertEqual(str(self.shop), "Test Shop - testuser")
        self.assertTrue(isinstance(self.shop.id, uuid.UUID))

    def test_shop_fields(self):
        self.assertEqual(self.shop.name, 'Test Shop')
        self.assertEqual(self.shop.address, '123 Test Street')
        self.assertEqual(self.shop.opening_time, time(9, 0))
        self.assertEqual(self.shop.closing_time, time(17, 0))
        self.assertEqual(self.shop.owner, self.user)

class ShopProductModelTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.role = 'apoteker'
        self.user.save()

        # Create test shop
        self.shop = ShopProfile.objects.create(
            owner=self.user,
            name='Test Shop',
            address='123 Test Street',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )

        # Create test drug
        self.drug = DrugEntry.objects.create(
            name='Test Drug',
            desc='Test Description',
            price=Decimal('10.00'),
            category='OTC'
        )

        # Create shop product relationship
        self.shop_product = ShopProduct.objects.create(
            shop=self.shop,
            product=self.drug,
            stock=100
        )

    def test_shop_product_creation(self):
        self.assertTrue(isinstance(self.shop_product, ShopProduct))
        self.assertEqual(
            str(self.shop_product),
            "Test Drug at Test Shop"
        )

    def test_shop_product_fields(self):
        self.assertEqual(self.shop_product.stock, 100)
        self.assertEqual(self.shop_product.shop, self.shop)
        self.assertEqual(self.shop_product.product, self.drug)

class ShopViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.role = 'apoteker'
        self.user.save()

        # Create test shop
        self.shop = ShopProfile.objects.create(
            owner=self.user,
            name='Test Shop',
            address='123 Test Street',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )

        # Create test drug
        self.drug = DrugEntry.objects.create(
            name='Test Drug',
            desc='Test Description',
            price=Decimal('10.00'),
            category='OTC'
        )

    def test_shop_list_view(self):
        response = self.client.get(reverse('shop:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop_list.html')

    def test_shop_profile_view(self):
        response = self.client.get(
            reverse('shop:profile', kwargs={'shop_id': self.shop.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/profile.html')

    def test_create_shop_view(self):
        # Test unauthorized access (not logged in)
        response = self.client.get(reverse('shop:create_shop'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

        # Test authorized access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('shop:create_shop'))
        self.assertEqual(response.status_code, 200)

        # Test shop creation
        shop_data = {
            'name': 'New Test Shop',
            'address': '456 New Street',
            'opening_time': '09:00',
            'closing_time': '17:00'
        }
        response = self.client.post(reverse('shop:create_shop'), shop_data)
        self.assertEqual(response.status_code, 302)  # Redirects after creation
        self.assertTrue(
            ShopProfile.objects.filter(name='New Test Shop').exists()
        )

    def test_delete_shop(self):
        # Login as shop owner
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request (confirmation page)
        response = self.client.get(
            reverse('shop:delete_shop', kwargs={'shop_id': self.shop.id})
        )
        self.assertEqual(response.status_code, 200)
        
        # Test POST request (actual deletion)
        response = self.client.post(
            reverse('shop:delete_shop', kwargs={'shop_id': self.shop.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirects after deletion
        self.assertFalse(ShopProfile.objects.filter(id=self.shop.id).exists())

class ShopPermissionsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create apoteker user
        self.apoteker = User.objects.create_user(
            username='apoteker',
            email='apoteker@example.com',
            password='testpass123'
        )
        self.apoteker.role = 'apoteker'
        self.apoteker.save()

        # Create customer user
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='testpass123'
        )
        self.customer.role = 'customer'
        self.customer.save()

        # Create test shop
        self.shop = ShopProfile.objects.create(
            owner=self.apoteker,
            name='Test Shop',
            address='123 Test Street',
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )

    def test_create_shop_permissions(self):
        # Test customer can't create shop
        self.client.login(username='customer', password='testpass123')
        response = self.client.get(reverse('shop:create_shop'))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test apoteker can create shop
        self.client.login(username='apoteker', password='testpass123')
        response = self.client.get(reverse('shop:create_shop'))
        self.assertEqual(response.status_code, 200)

    def test_edit_shop_permissions(self):
        # Test customer can't edit shop
        self.client.login(username='customer', password='testpass123')
        response = self.client.get(
            reverse('shop:edit_profile', kwargs={'shop_id': self.shop.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirects to login/error

        # Test apoteker (owner) can edit shop
        self.client.login(username='apoteker', password='testpass123')
        response = self.client.get(
            reverse('shop:edit_profile', kwargs={'shop_id': self.shop.id})
        )
        self.assertEqual(response.status_code, 200)
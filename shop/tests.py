from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ShopProfile, ShopProduct
from product.models import DrugEntry


class ShopViewsTestCase(TestCase):
    def setUp(self):
        # Create a user with the role 'apoteker'
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.user.role = 'apoteker'  # Set user role (assuming role is an attribute of User)
        self.user.save()  # Save the user to apply changes

        # Create a shop profile
        self.shop = ShopProfile.objects.create(
            owner=self.user,
            name='Test Shop',
            address='123 Test St',
            opening_time='09:00:00',
            closing_time='21:00:00',
        )

        # Create a test product
        self.product = DrugEntry.objects.create(
            name='Test Product',
            category='Test Category'
        )

        # Associate the product with the shop
        ShopProduct.objects.create(
            shop=self.shop,
            product=self.product,
            stock=10,
            selling_price=100.00
        )

    def test_create_shop_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('shop:create_shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/create_shop.html')

        response = self.client.post(reverse('shop:create_shop'), {
            'name': 'New Shop',
            'address': '456 New St',
            'opening_time': '10:00:00',
            'closing_time': '22:00:00',
            # Include other required fields from ShopProfileForm if necessary
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertTrue(ShopProfile.objects.filter(name='New Shop').exists())

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('shop:edit_profile', args=[self.shop.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/edit_profile.html')

        response = self.client.post(reverse('shop:edit_profile', args=[self.shop.id]), {
            'name': 'Updated Shop Name',
            'address': 'Updated Address',
            'opening_time': '08:00:00',
            'closing_time': '20:00:00',
            # Include other required fields from ShopProfileForm if necessary
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.shop.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.shop.name, 'Updated Shop Name')

    def test_delete_shop_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('shop:delete_shop', args=[self.shop.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/delete_shop.html')

        response = self.client.post(reverse('shop:delete_shop', args=[self.shop.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect after deletion
        self.assertFalse(ShopProfile.objects.filter(id=self.shop.id).exists())

    def test_manage_products_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('shop:manage_products', args=[self.shop.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/manage_products.html')

    def test_delete_product_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('shop:delete_product', args=[self.shop.id, self.product.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect after deletion
        self.assertFalse(ShopProduct.objects.filter(product=self.product, shop=self.shop).exists())

    def test_shop_list_view(self):
        response = self.client.get(reverse('shop:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop_list.html')

    def test_shop_profile_view(self):
        response = self.client.get(reverse('shop:profile', args=[self.shop.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/profile.html')


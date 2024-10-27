from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from daftar_favorit.models import Favorite
from product.models import DrugEntry
import uuid
import json

class FavoriteTests(TestCase):
    def setUp(self):
        # Set up test client
        self.client = Client()
        
        # Create test user
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test product
        self.product = DrugEntry.objects.create(
            name='Test Medicine',
            price=10000,
            category='Test Category',
            drug_type='Test Type',
            drug_form='Test Form',
            desc='Test Description'
        )
        
        # Create test favorite
        self.favorite = Favorite.objects.create(
            user=self.user,
            product=self.product
        )
        
        # Login the test user
        self.client.login(username='testuser', password='testpass123')

    def test_favorite_model(self):
        """Test for Favorite model"""
        favorite = Favorite.objects.get(id=self.favorite.id)
        self.assertEqual(str(favorite), f"{self.user.username} - {self.product.name}")
        self.assertTrue(isinstance(favorite.id, uuid.UUID))
        
    def test_show_favorite_view(self):
        """Test show_favorite view"""
        response = self.client.get(reverse('daftar_favorite:show_favorite'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorite.html')
        self.assertTrue('favorite_items' in response.context)
        
    def test_show_json_view(self):
        """Test show_json view"""
        response = self.client.get(reverse('daftar_favorite:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
    def test_add_to_favorites(self):
        """Test adding item to favorites"""
        # Create new product to add to favorites
        new_product = DrugEntry.objects.create(
            name='New Medicine',
            price=20000,
            category='New Category',
            drug_type='New Type',
            drug_form='New Form',
            desc='New Description'
        )
        
        response = self.client.post(
            reverse('daftar_favorite:add_to_favorite', kwargs={'product_id': new_product.id})
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(
            Favorite.objects.filter(user=self.user, product=new_product).exists()
        )
        
    def test_delete_favorite(self):
        """Test deleting item from favorites"""
        response = self.client.post(
            reverse('daftar_favorite:delete_favorite', 
                   kwargs={'product_id': self.favorite.id})
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertFalse(
            Favorite.objects.filter(id=self.favorite.id).exists()
        )
        
    def test_get_favorite_count(self):
        """Test getting favorite count"""
        response = self.client.get(reverse('daftar_favorite:get_favorite_count'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['favorite_count'], 1)
        
    def test_check_favorite_status(self):
        """Test checking favorite status"""
        response = self.client.get(
            reverse('daftar_favorite:check_favorite_status', 
                   kwargs={'product_id': self.product.id})
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['is_favorite'])
   
        
    def test_unauthorized_access(self):
        """Test accessing views without authentication"""
        self.client.logout()
        
        # Test add to favorites
        response = self.client.post(
            reverse('daftar_favorite:add_to_favorite', 
                   kwargs={'product_id': self.product.id})
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        
        # Test delete favorite
        response = self.client.post(
            reverse('daftar_favorite:delete_favorite', 
                   kwargs={'product_id': self.favorite.id})
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to login
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from product.models import DrugEntry as Produk
from resep.models import Resep
from django.utils import timezone
from decimal import Decimal

User = get_user_model()


class ResepViewsTest(TestCase):

    def setUp(self):
        # Set up user, client, and initial data
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        
        # Create product entries
        self.product1 = Produk.objects.create(name="Produk1", price=Decimal('10000.00'), image="image1.jpg")
        self.product2 = Produk.objects.create(name="Produk2", price=Decimal('20000.00'), image="image2.jpg")

        # Create initial resep entry
        self.resep = Resep.objects.create(user=self.user, product=self.product1, amount=2)

    def test_show_resep(self):
        # Test the show_resep view to display correct data
        url = reverse('resep:show_resep')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produk1")
        self.assertContains(response, "Rp 20000")
        self.assertContains(response, "Total Harga")

    def test_add_to_resep(self):
        # Test adding a product to resep or updating amount if already exists
        url = reverse('resep:add_to_resep', args=[self.product2.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Check if the product was added to the resep
        self.assertEqual(Resep.objects.filter(user=self.user, product=self.product2).count(), 1)
        self.assertEqual(Resep.objects.get(user=self.user, product=self.product2).amount, 1)

    def test_update_amount_increase(self):
        # Test updating the amount of a product in resep (increase)
        url = reverse('resep:update_amount')
        response = self.client.post(url, {'resep_id': self.resep.id, 'action': 'increase'})

        self.assertEqual(response.status_code, 200)
        self.resep.refresh_from_db()
        self.assertEqual(self.resep.amount, 3)
        self.assertEqual(response.json()['deleted'], False)

    def test_update_amount_decrease(self):
        # Test updating the amount of a product in resep (decrease)
        url = reverse('resep:update_amount')
        response = self.client.post(url, {'resep_id': self.resep.id, 'action': 'decrease'})

        self.assertEqual(response.status_code, 200)
        self.resep.refresh_from_db()
        self.assertEqual(self.resep.amount, 1)
        self.assertEqual(response.json()['deleted'], False)

    def test_update_amount_decrease_delete(self):
        # Test decreasing the amount when it's already at the minimum (1), which should delete the product
        self.resep.amount = 1
        self.resep.save()

        url = reverse('resep:update_amount')
        response = self.client.post(url, {'resep_id': self.resep.id, 'action': 'decrease'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['deleted'], True)
        self.assertEqual(Resep.objects.filter(id=self.resep.id).count(), 0)

    def test_clear_recipes(self):
        # Test clearing all resep entries for a user
        url = reverse('resep:clear_recipes')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(Resep.objects.filter(user=self.user).count(), 0)

    def test_update_amount_increase_max_limit(self):
        # Atur jumlah produk ke 99, lalu coba menambahnya
        self.resep.amount = 99
        self.resep.save()

        url = reverse('resep:update_amount')
        response = self.client.post(url, {'resep_id': self.resep.id, 'action': 'increase'})

        self.assertEqual(response.status_code, 200)
        self.resep.refresh_from_db()
        # Pastikan jumlah tetap 99
        self.assertEqual(self.resep.amount, 99)

    def test_update_amount_invalid_resep_id(self):
        # Gunakan ID yang tidak ada dalam basis data
        invalid_id = '12345678-1234-5678-1234-567812345678'
        url = reverse('resep:update_amount')
        response = self.client.post(url, {'resep_id': invalid_id, 'action': 'increase'})

        self.assertEqual(response.status_code, 404)

    def test_add_existing_product_to_resep(self):
        # Tambahkan produk yang sudah ada dalam resep
        url = reverse('resep:add_to_resep', args=[self.product1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.resep.refresh_from_db()
        # Pastikan jumlahnya diperbarui, bukan menambah entri baru
        self.assertEqual(self.resep.amount, 3)  # Sebelumnya sudah 2, jadi bertambah menjadi 3
        self.assertEqual(Resep.objects.filter(user=self.user, product=self.product1).count(), 1)

    def test_show_resep_redirect_if_not_logged_in(self):
        # Logout pengguna yang sudah login
        self.client.logout()
        url = reverse('resep:show_resep')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_add_to_resep_redirect_if_not_logged_in(self):
        # Logout pengguna yang sudah login
        self.client.logout()
        url = reverse('resep:add_to_resep', args=[self.product1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_update_amount_json_response_format(self):
        url = reverse('resep:update_amount')
        response = self.client.post(url, {'resep_id': self.resep.id, 'action': 'increase'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('amount', data)
        self.assertIsInstance(data['amount'], int)
        self.assertIn('total_price', data)
        self.assertIsInstance(data['total_price'], float)
        self.assertIn('deleted', data)
        self.assertIsInstance(data['deleted'], bool)

    def test_clear_recipes_after_checkout(self):
        # Pastikan terdapat produk di resep
        Resep.objects.create(user=self.user, product=self.product2, amount=1)
        self.assertEqual(Resep.objects.filter(user=self.user).count(), 2)
        
        # Lakukan clear recipes
        url = reverse('resep:clear_recipes')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Resep.objects.filter(user=self.user).count(), 0)

from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User
from product.models import DrugEntry
from django.core.files.uploadedfile import SimpleUploadedFile
import json

class DrugEntryModelTests(TestCase):

    def setUp(self):
        # Set up a DrugEntry instance for model tests
        self.drug = DrugEntry.objects.create(
            name="Aspirin",
            desc="Pain reliever",
            category="Pain Relief",
            drug_type="Modern",
            drug_form="Tablet",
            price=1000
        )

    def test_drug_entry_creation(self):
        """Test if a DrugEntry instance is created successfully."""
        self.assertEqual(self.drug.name, "Aspirin")
        self.assertEqual(self.drug.desc, "Pain reliever")
        self.assertEqual(self.drug.price, 1000)

    def test_drug_str_representation(self):
        """Test the string representation of the DrugEntry model."""
        self.assertEqual(str(self.drug), "Aspirin")


class DrugEntryViewTests(TestCase):

    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username="user", nama="A User", password="123password", role="apoteker")
        self.client.login(username="user", password="123password")
        
        # Set up a sample drug entry
        self.drug = DrugEntry.objects.create(
            name="Paracetamol",
            desc="Fever reducer",
            category="Pain Relief",
            drug_type="Modern",
            drug_form="Tablet",
            price=5000
        )

    def test_show_main(self):
        """Test the main page displaying all products."""
        url = reverse('product:show_main')
        response = self.client.get(url)
        
        # Check status and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_products.html')
        


    def test_create_drug_ajax_view(self):
        """Test the create drug AJAX view."""
        url = reverse('product:create_drug_ajax')
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'name': "Ibuprofen",
            'desc': "Pain reliever",
            'category': "Pain Relief",
            'drug_type': "Modern",
            'drug_form': "Capsule",
            'price': 2000,
            'image': image
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b"CREATED")

    def test_edit_drug_ajax_view(self):
        """Test editing a drug entry via AJAX."""
        url = reverse('product:edit_drug_ajax', args=[self.drug.id])
        data = {
            'name': "Updated Paracetamol",
            'desc': "Updated description",
            'price': 6000
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.drug.refresh_from_db()
        self.assertEqual(self.drug.name, "Updated Paracetamol")
        self.assertEqual(self.drug.price, 6000)

    def test_delete_drug_view(self):
        """Test deleting a drug entry."""
        url = reverse('product:delete_drug', args=[self.drug.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Should redirect on successful deletion
        self.assertFalse(DrugEntry.objects.filter(id=self.drug.id).exists())

    def test_show_drug_view(self):
        """Test showing a single drug's details."""
        url = reverse('product:show_drug', args=[self.drug.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, self.drug.name)

    def test_show_json_view(self):
        """Test JSON serialization of all drugs."""
        url = reverse('product:show_json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['fields']['name'], "Paracetamol")

    def test_show_json_by_id_view(self):
        """Test JSON serialization of a drug by ID."""
        url = reverse('product:show_json_by_id', args=[self.drug.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['fields']['name'], "Paracetamol")

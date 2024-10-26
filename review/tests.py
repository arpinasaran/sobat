import uuid
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Review
from product.models import DrugEntry as Produk
from authentication.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class reviewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", nama="A User", password="123password", role="pengguna")
        self.client.login(username="user", password="123password")
        self.product = Produk.objects.create(
            name="A Product",
            desc="A description",
            category="Modern",
            drug_type="Something",
            drug_form="Capsule",
            price=10000,
            availibility=True,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
        self.review = Review.objects.create(
            user = self.user,
            product = self.product,
            rating = 2.5,
            comment = "This is a disappointing product."
        )

    def test_main_review_url_is_exist(self):
        response = Client().get(reverse('review:reviews', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_main_review_page_using_reviews_template(self):
        response = Client().get(reverse('review:reviews', args=[self.product.id]))
        self.assertTemplateUsed(response, 'reviews.html')

    def test_nonexistent_page(self):
        response = Client().get('/nonexistent/')
        self.assertEqual(response.status_code, 404)
    
    def test_review_display_in_reviews_template(self):
        response = self.client.get(reverse('review:reviews', args=[self.product.id]))
        self.assertContains(response, self.review.comment)
        self.assertContains(response, f"{self.review.rating}/5")
        self.assertContains(response, self.user.nama)

    def test_add_review_button_shown_to_pengguna(self):
        response = self.client.get(reverse('review:reviews', args=[self.product.id]))
        self.assertContains(response, 'Add Review')

    def test_edit_delete_buttons_for_reviewer(self):
        response = self.client.get(reverse('review:reviews', args=[self.product.id]))
        self.assertContains(response, reverse('review:edit_review', args=[self.product.id, self.review.id]))
        self.assertContains(response, reverse('review:delete_review', args=[self.product.id, self.review.id]))

    def test_create_a_review(self):
        review = Review.objects.create(
            user = self.user,
            product = self.product,
            rating = 4.7,
            comment = "This is a good product!"
        )
        self.assertIsInstance(review.id, uuid.UUID)
        self.assertEqual(review.rating, 4.7)
        self.assertEqual(review.comment, "This is a good product!")
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
    
    def test_review_str_method(self):
        review = Review.objects.create(
            user = self.user,
            product = self.product,
            rating = 4,
            comment="Worth the price!"
        )
        self.assertEqual(str(review), f"{self.product.name} Review: 4 Star(s) - {self.user.nama}")
    
    def test_review_date_creation(self):
        review = Review.objects.create(
            user = self.user,
            product = self.product,
            rating = 4,
            comment="Worth the price!"
        )
        self.assertEqual(review.date_created, timezone.now().date())
    
    def test_rating_field_validation(self):
        review = Review.objects.create(
            user = self.user,
            product = self.product,
            rating = 9.3,
            comment="Intentionally invalid rating!"
        )
        with self.assertRaises(ValidationError):
            review.full_clean()
    
    def test_delete_review(self):
        review = Review.objects.create(
            user = self.user,
            product = self.product,
            rating = 5.0,
            comment="Worth the price!"
        )
        review_id = review.id
        review.delete()
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(id=review_id)
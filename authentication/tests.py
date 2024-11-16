from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelTests(TestCase):

    def test_create_user_with_valid_data(self):
        # Test creating a user with valid data
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            nama='Test User',
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.nama, 'Test User')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_user_with_invalid_role(self):
        # Test creating a user with an invalid role
        with self.assertRaises(ValidationError):
            user = User(
                username='invaliduser',
                password='testpass123',
                nama='Invalid User',
                role='invalid_role'  # Invalid role
            )
            user.full_clean()  # This should raise a ValidationError

    def test_user_string_representation(self):
        # Test the string representation of the user
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            nama='Test User',
            role='pengguna'
        )
        self.assertEqual(str(user), 'Test User')

    def test_create_superuser(self):
        # Test creating a superuser
        superuser = User.objects.create_superuser(
            username='superuser',
            password='superpass123',
            nama='Super User',
            role='pengguna'
        )
        self.assertEqual(superuser.username, 'superuser')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password('superpass123'))

    def test_create_user_without_role(self):
        # Test creating a user without specifying a role
        user = User.objects.create_user(
            username='noroleuser',
            password='norolepass123',
            nama='No Role User'
        )
        self.assertEqual(user.role, '')

from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

class UserManagerTests(TestCase):
    
    def test_create_user(self):# username is None for the AbstractUser option
        # username does not exist for the AbstractBaseUser option
        User = get_user_model() 
        user = User.objects.create_user(username='normal', email='daniel@user.com', password='foo')
        self.assertEqual(user.email, 'daniel@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.username, 'normal')  # Check if username is set correctly
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', email='', password="foo")

    
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='super', email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.username, 'super')  # Check if username is set correctly
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='super', email='super@user.com', password='foo', is_superuser=False)
            

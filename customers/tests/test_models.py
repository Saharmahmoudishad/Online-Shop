from django.core.exceptions import ValidationError
from django.test import TestCase
from customers.models import CustomUser, Address
from model_bakery import baker


class TestCustomUserModel(TestCase):
    def setUp(self):
        self.customuser = baker.make(CustomUser, firstname='sahar', lastname='mahmoodi')

    def test_model_str(self):
        """Test __str__ method"""
        self.assertEquals(str(self.customuser), 'sahar_mahmoodi')

    def test_soft_delete(self):
        """Test soft_delete method logically delete  a user"""
        self.assertFalse(self.customuser.is_deleted)
        self.customuser.delete()
        self.assertTrue(self.customuser.is_deleted)

    def test_hard_delete(self):
        """Test hard_delete method delete a user from database"""
        self.assertFalse(self.customuser.is_deleted)
        self.customuser.hard_delete()
        self.assertRaises(CustomUser.DoesNotExist)

    def test_has_perm_admin(self):
        """Test has_perm method for an admin user."""
        self.customuser.is_admin = True
        self.assertTrue(self.customuser.has_perm('some_permission'))

    def test_has_perm_active_user(self):
        """Test has_perm method for an active user."""
        self.customuser.is_admin = True
        self.customuser.is_active = True
        self.assertTrue(self.customuser.has_perm('some_permission'))

    def test_has_perm_inactive_user(self):
        """Test has_perm method for an inactive user."""
        self.customuser.is_admin = False
        self.customuser.is_active = True
        self.assertFalse(self.customuser.has_perm('some_permission'))

    def test_has_module_perms(self):
        """Test has_module_perms method."""
        app_label = 'some_app'
        self.assertTrue(self.customuser.has_module_perms(app_label))

    def test_is_staff_admin(self):
        """Test is_staff property for an admin user."""
        self.customuser.is_admin = True
        self.assertTrue(self.customuser.is_staff)

    def test_is_staff_non_admin(self):
        """Test is_staff property for a non-admin user."""
        self.customuser.is_admin = False
        self.assertFalse(self.customuser.is_staff)


class TestAddressModel(TestCase):
    def setUp(self):
        self.address = baker.make(Address, postcode='12345678901')

    def test_invalid_postcode_length(self):
        """Attempt to create an address with an invalid postcode length"""
        self.assertRaises(Address.DoesNotExist)

    def setUp(self):
        self.address = baker.make(Address, )

    def test_valid_address(self):
        """T Create a valid address"""
        self.assertEqual(Address.objects.count(), 1)

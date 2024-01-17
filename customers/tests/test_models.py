from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from core.models import Province, City
from customers.models import CustomUser, Address
from model_bakery import baker


class TestCustomUserModel(TestCase):
    def setUp(self):
        self.customuser = baker.make(CustomUser, firstname='sahar', lastname='mahmoodi')
        self.sample_instance = CustomUser.objects.create_user(phonenumber="+989123456799", email="test@example.com",
                                                              firstname="John", lastname="Doe", how_know_us="Ins")

    def test_valid_instance(self):
        """Test if the sample instance is valid"""
        self.assertIsNone(self.sample_instance.full_clean())

    def test_invalid_phonenumber(self):
        """Test an invalid phone number"""
        invalid_instance = CustomUser.objects.create_user(phonenumber="invalid_number", email="testa@example.com",
                                                          firstname="John", lastname="Doe", how_know_us="Ins")
        with self.assertRaises(ValidationError) as context:
            invalid_instance.full_clean()
            self.assertIn("Invalid phone number format. Example: +989123456789 or 09123456789",
                          str(context.exception))

    def test_invalid_email(self):
        invalid_instance = CustomUser.objects.create_user(phonenumber="+989123456789", email="invalid_email",
                                                          firstname="John", lastname="Doe", how_know_us="Ins")
        with self.assertRaises(ValidationError) as context:
            invalid_instance.full_clean()
        self.assertIn("Enter a valid email address.", str(context.exception))

    #
    def test_unique_email(self):
        with self.assertRaises(IntegrityError) as context:
            CustomUser.objects.create_user(phonenumber="+989987654321", email="test@example.com",
                                           firstname="Jane", lastname="Doe", how_know_us="Referral")

        self.assertIn('duplicate key value violates unique constraint "customers_customuser_email_key"',
                      str(context.exception))

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
        self.user = CustomUser.objects.create_user(phonenumber="+989123456799", email="test@example.com",
                                                   firstname="John", lastname="Doe", how_know_us="Ins")
        self.province = Province.objects.create(name='TestProvince')
        self.city = City.objects.create(name='TestCity', province=self.province)
        self.address1 = baker.make(Address, postcode='12345678901', city=self.city)

    def test_invalid_postcode_length(self):
        """Attempt to create an address with an invalid postcode length"""
        self.assertRaises(Address.DoesNotExist)

    def test_address_created(self):
        """Test that Address model is created correctly."""
        self.address2 = Address.objects.create(user=self.user, province=self.province, city=self.city,
                                               address='TestAddress', postcode='12345')
        self.assertEqual(self.address2.user, self.user)
        self.assertEqual(self.address2.city, self.city)
        self.assertEqual(self.address2.address, 'TestAddress')
        self.assertEqual(self.address2.postcode, '12345')

    def test_valid_address(self):
        """T Create a valid address"""
        self.assertEqual(Address.objects.count(), 1)

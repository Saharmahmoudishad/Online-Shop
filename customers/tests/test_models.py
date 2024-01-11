from django.test import TestCase
from customers.models import CustomUser
from model_bakery import baker


class TestCustomUserModel(TestCase):
    def setUp(self):
        self.customuser = baker.make(CustomUser, firstname='sahar', lastname='mahmoodi')

    def test_model_str(self):
        self.assertEquals(str(self.customuser), 'sahar_mahmoodi')

    def test_soft_delete(self):
        self.assertFalse(self.customuser.is_deleted)
        self.customuser.delete()
        self.assertTrue(self.customuser.is_deleted)

    def test_hard_delete(self):
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
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from customers.views import RequestRegisterView


# class TestRequestRegisterView(TestCase):
#     def setUp(self):
#         self.user
#         self.factory = RequestFactory()
class TestRequestRegisterView(TestCase):
    def setUp(self):
        self.user_data = {'phonenumber': '09126308147', 'email': 'test@example.com', 'password': 'testpassword'}
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_form_valid_existing_user(self):
        # Setup
        url = reverse(RequestRegisterView)  # replace 'your_view_name' with the actual name of your view
        data = {'email': 'test@example.com'}

        # Test
        response = self.client.post(url, data)

        # Assert
    #     self.assertRedirects(response, reverse('customers:verify_login_code'))
    #     self.assertIn('user_registration_info', self.client.session)
    #
    #     # Check if email is sent
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertIn('Your OTP code is', mail.outbox[0].body)
    #
    # def test_form_valid_new_user(self):
    #     # Setup
    #     url = reverse('your_view_name')  # replace 'your_view_name' with the actual name of your view
    #     data = {'email': 'newuser@example.com'}
    #
    #     # Test
    #     response = self.client.post(url, data)
    #
    #     # Assert
    #     self.assertRedirects(response, reverse('core:home'))
    #     self.assertIn('user_registration_info', self.client.session)
    #
    #     # Check if email is sent
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertIn('The authentication confirmation link', mail.outbox[0].body)

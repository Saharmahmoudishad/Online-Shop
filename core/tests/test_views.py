from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from core.views import IndexView
from customers.models import CustomUser
from model_bakery import baker


class TestIndexView(TestCase):
    def setUp(self):
        self.customuser = baker.make(CustomUser,)
        self.factory = RequestFactory()

    def test_home_user_authenticated(self):
        request = self.factory.get(reverse('home:home'))
        request.user = self.customuser
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code,200)

    def test_home_user_anonymous(self):
        request = self.factory.get(reverse('core:home'))
        request.user = AnonymousUser()
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code,200)


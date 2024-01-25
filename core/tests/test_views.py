from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from core.views import IndexView, ContactUsView
from customers.models import CustomUser
from model_bakery import baker


class TestIndexView(TestCase):
    def setUp(self):
        self.customuser = baker.make(get_user_model())
        self.factory = RequestFactory()

    def test_home_user_authenticated(self):
        request = self.factory.get(reverse('core:home'))
        request.user = self.customuser
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_home_user_anonymous(self):
        request = self.factory.get(reverse('core:home'))
        request.user = AnonymousUser()
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_cache_used(self):
        cache.clear()

        request = self.factory.get(reverse('core'
                                           ':home'))
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        with self.assertNumQueries(1):
            response_cached = IndexView.as_view()(request)
            self.assertEqual(response_cached.status_code, 200)


class TestContactUsView(TestCase):
    def setUp(self):
        self.customuser = baker.make(CustomUser, )
        self.factory = RequestFactory()

    def test_home_user_authenticated(self):
        request = self.factory.get(reverse('core:home'))
        request.user = self.customuser
        response = ContactUsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_home_user_anonymous(self):
        request = self.factory.get(reverse('core:home'))
        request.user = AnonymousUser()
        response = ContactUsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views import View


# Create your views here.
class CartView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class CartAddView(PermissionRequiredMixin, View):

    def post(self, request):
        pass


class CartRemoveView(View):
    def get(self, request):
        pass


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request):
        pass


class OrderCreateView(LoginRequiredMixin, View):

    def get(self, request):
        pass

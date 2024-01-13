from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('register/', views.CustomerRegisterView.as_view(), name='customer_register'),
    path('verify/', views.CustomerRegisterVerifyCodeView.as_view(), name='verify_registeration_code'),
]

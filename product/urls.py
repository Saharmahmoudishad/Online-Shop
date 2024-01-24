from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
     path('/', views.AllProductView.as_view(), name='products'),
]
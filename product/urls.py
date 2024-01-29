from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
     path('', views.AllProductView.as_view(), name='products'),
     path('category/<slug:slug>', views.AllProductView.as_view(), name='category_filter'),
     path('product_detail/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),

]
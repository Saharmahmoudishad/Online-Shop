from django.urls import path
from .views import CartView, CheckOutView, CheckOutEndView
from .API import views

app_name = 'orders'
urlpatterns = [
    # django Views************************************#
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('checkout/paid/', CheckOutEndView.as_view(), name='checkout_paid'),
    # API Views****************************************#
    path('create/', views.ReceiptCreateView.as_view(), name='order_create'),
    path('create/update/<int:order_id>', views.ReceiptUpdateView.as_view(), name='order_create'),
    path('create/addiscount/', views.ReceiptAddDiscountView.as_view(), name='oder_add_discount'),
    path('create/receipt/delete/', views.ReceiptDeleteView.as_view(), name='oder_delete'),
    path('cart/final/', views.CartProductView.as_view(), name='cart_final_product'),
    path('cart/update/<int:variant_id>/', views.CartUpdateProductView.as_view(), name='cart_update_product'),
    path('cart/<int:product_id>/', views.CartAddProductView.as_view(), name='cart_add_product'),
    path('cart/remove/<int:variant_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('checkout/detail/', views.CheckOutView.as_view(), name='checkout_detail'),
    path('checkout/setaddress/', views.CheckOutSetAddressView.as_view(), name='checkout_set_address'),
    path('checkout/newaddress/', views.NewAddressView.as_view(), name='checkout_set_new_address'),
    path('checkout/delivery/', views.DeliveryMethodView.as_view(), name='checkout_delivery'),


]

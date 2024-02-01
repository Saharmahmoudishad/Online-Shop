from django.urls import path
from . import views
from .views import ReplyProductCommentView

app_name = 'product'
urlpatterns = [
    path('', views.AllProductView.as_view(), name='products'),
    path('category/<slug:slug>/', views.AllProductView.as_view(), name='category_filter'),
    path('product_detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_comment_reply/<str:product_slug>/<int:comment_id>/', ReplyProductCommentView.as_view(), name='reply_product_comment'),
    path('like/<int:product_id>/', views.ProductLikeView.as_view(), name='product_like'),
]

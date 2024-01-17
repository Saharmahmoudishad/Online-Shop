from django.urls import path

from . import views
from .views import index_view_cached

app_name = 'core'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('', index_view_cached, name='index'),
]

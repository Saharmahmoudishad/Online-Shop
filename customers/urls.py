from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('register/', views.RequestRegisterView.as_view(), name='request_register_by_email'),
    # path('verify/', views.CustomerRegisterVerifyCodeView.as_view(), name='verify_registeration_code'),
    # path('verify/', views.CustomerRegisterVerifyCodeView.as_view(), name='verify_registeration_complete'),
    path('confrim_email/<uidb64>/<token>', views.CompleteRegisterByEmailView.as_view(), name='complete_registeration_by_email'),
    path('verify_code/', views.CompleteRegisterVerifyCodeView.as_view(), name='verify_registeration_code'),


]

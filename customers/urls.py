from django.urls import path
from . import views


app_name = 'customers'
urlpatterns = [
    path('register/', views.RequestRegisterView.as_view(), name='request_register_by_email'),
    path('confrim_email/<uidb64>/<token>', views.CompleteRegisterByEmailView.as_view(), name='complete_registeration_by_email'),
    path('registerByphone/', views.RequestRegisterByPhoneView.as_view(), name='request_register_by_phone'),
    path('verify_login_code_byemail/', views.LoginVerifyCodeView.as_view(), name='verify_login_code'),
    path('verify_code/', views.CompleteRegisterVerifyCodeView.as_view(), name='verify_registeration_code'),
    path('login/', views.UserLoginByPassView.as_view(), name='user_login_by_pass'),
    path('logout/', views.UserLogoutView.as_view(), name='User_logout'),
]
urlpatterns += [
path('reset_pass/', views.UserPasswordResetView.as_view(), name='reset_password'),
path('reset_done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_completed'),
]
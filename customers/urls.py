from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .API.views import HandlingToken

# from rest_framework.authtoken import views as auth_token


app_name = 'customers'
urlpatterns = [
    path('register/', views.RequestRegisterView.as_view(), name='request_register_by_email'),
    path('confrim_email/<uidb64>/<token>', views.CompleteRegisterByEmailView.as_view(),
         name='complete_registeration_by_email'),
    path('registerByphone/', views.RequestRegisterByPhoneView.as_view(), name='request_register_by_phone'),
    path('verify_login_code_byemail/', views.LoginVerifyCodeView.as_view(), name='verify_login_code'),
    path('verify_code/', views.CompleteRegisterVerifyCodeView.as_view(), name='verify_registeration_code'),
    path('login/<identifier>/', views.UserLoginByPassView.as_view(), name='user_login_by_pass'),
    path('logout/', views.UserLogoutView.as_view(), name='User_logout'),
    # tokenAuthentication for API*****************************************************************************************#
    # path('api-token-auth/', auth_token.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/', HandlingToken.as_view(), name='token_handle'),
]
urlpatterns += [
    path('reset_pass/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset_done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_completed'),
]

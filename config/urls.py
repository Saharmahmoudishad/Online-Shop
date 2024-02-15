"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from core.views import ChangeLangView
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [   path('schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                  path('change-lang/', ChangeLangView.as_view(), name='change_lang'),
                  path('', include('social_django.urls', namespace='social')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('core.urls', namespace='home')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('category/', include('product.urls', namespace='product')),
    path('orders/', include('orders.urls', namespace='orders')),
)
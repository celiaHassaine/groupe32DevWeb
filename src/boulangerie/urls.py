"""boulangerie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('', include('news.urls')),
    path('api/auth/login/', obtain_jwt_token, name='api-login'),
    path('produits/', include('produits.urls')),
    path('contact/', views.contact, name='contact'),
    path('commande/', views.commande, name='commande'),
    path('sandwich/', views.sandwich, name='sandwich'),
    path('api/news/', include('news.api.urls', namespace='api-news')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

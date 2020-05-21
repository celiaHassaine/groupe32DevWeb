from django.urls import path

from . import views

urlpatterns = [
    path('', views.liste_produits, name='Liste des produits'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.liste_categories, name='Liste des catégories'),
    path('categorie/<int:categorie_id>', views.categorie, name='Catégorie'),
    path('detail', views.detail),
    path('commande/detail', views.commande_detail),
    path('commande/ajouter', views.commande_ajouter),
    path('commande/finaliser', views.commande_finaliser),
]

from django.contrib import admin
from .models import Attribut, Valeur, Produit, Commande, ProduitAttribut, Categorie

# Register your models here.

admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Attribut)
admin.site.register(Valeur)
admin.site.register(Commande)

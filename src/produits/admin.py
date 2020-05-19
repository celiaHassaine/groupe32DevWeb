from django.contrib import admin
from .models import Attribut, Valeur, Produit, Commandes, ProdAttr, Categorie

# Register your models here.

admin.site.register(Attribut)
admin.site.register(Valeur)
admin.site.register(Produit)
admin.site.register(Commandes)
admin.site.register(ProdAttr)
admin.site.register(Categorie)


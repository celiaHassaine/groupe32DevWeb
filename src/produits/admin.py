from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

from .models import Attribut, Valeur, Produit, Commande, ProduitAttribut, Categorie, ProduitAttributValeur

class ProduitAttributValeurInline(NestedStackedInline):
    model = ProduitAttributValeur
    extra = 0

class ProduitAttributInline(NestedStackedInline):
    model = ProduitAttribut
    extra = 0
    inlines = [
        ProduitAttributValeurInline,
    ]

class ProduitAdmin(NestedModelAdmin):
    inlines = [
        ProduitAttributInline,
    ]


admin.site.register(Categorie)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Attribut)
admin.site.register(Valeur)
admin.site.register(Commande)

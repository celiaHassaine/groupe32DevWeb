from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

from .models import Attribut, Valeur, Produit, Commande, ProduitAttribut, Categorie, ProduitAttributValeur, CommandeProduit


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


class ValeurInline(NestedStackedInline):
    model = Valeur
    extra = 0


class AttributAdmin(NestedModelAdmin):
    inlines = [
        ValeurInline,
    ]


admin.site.register(Categorie)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Attribut, AttributAdmin)
admin.site.register(Valeur)


class CommandeProduitInline(NestedStackedInline):
    model = CommandeProduit
    extra = 0


class CommandeAdmin(NestedModelAdmin):
    inlines = [
        CommandeProduitInline,
    ]


admin.site.register(Commande, CommandeAdmin)

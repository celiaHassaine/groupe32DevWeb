from django.contrib import admin
from .models import Attribut, Valeur, Produit, Commande, ProduitAttribut, Categorie

# Register your models here.


class ProduitAdmin(admin.ModelAdmin):
    fields = ('nom', 'prix', 'categorie', 'en_vente', 'description', 'image')
    list_display = ('nom', 'categorie', 'en_vente', 'prix')


admin.site.register(Categorie)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Attribut)
admin.site.register(Valeur)
admin.site.register(Commande)

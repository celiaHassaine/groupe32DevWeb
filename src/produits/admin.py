from django.contrib import admin
from .models import Attribut, Valeur, Produits, Commandes, ProdAttr

# Register your models here.

admin.site.register(Attribut)
admin.site.register(Valeur)
admin.site.register(Produits)
admin.site.register(Commandes)
admin.site.register(ProdAttr)

from django.shortcuts import render
from django.http import HttpResponse

from .models import Produit


# Create your views here.
def liste_produits(request):
    produits = Produit.objects.filter(en_vente=True)
    return render(request, 'produits.html', {
        'produits': produits,
    })

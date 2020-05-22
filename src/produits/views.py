from django.shortcuts import render

from .models import Categorie


# Create your views here.

def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'categories.html', {
        'categories': categories,
    })


def categorie(request, categorie_id):
    categorie = Categorie.objects.get(id=categorie_id)
    produits = categorie.produits.filter(en_vente=True)
    return render(request, 'produits.html', {
        'categorie': categorie,
        'produits': produits,
    })

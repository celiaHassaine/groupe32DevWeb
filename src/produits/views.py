import json

from django.shortcuts import render
from django.http import JsonResponse

from .models import Categorie, Produit


def detail(request):
    body = json.loads(request.body)
    produit = Produit.objects.get(id=body.get('produit_id'))
    data = {
        'produit': {
            'id': produit.id,
            'nom': produit.nom,
            'prix': produit.prix,
            'image': produit.image.url if produit.image else False,
        },
    }
    return JsonResponse(data)


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

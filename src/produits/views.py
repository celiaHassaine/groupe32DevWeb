import json

from django.shortcuts import render
from django.http import JsonResponse

from .models import Categorie, Produit, Commande, CommandeProduit


def commande_ajouter(request):
    uuid = request.COOKIES.get('commande_uuid')
    commande = Commande.objects.get(uuid=uuid)
    body = json.loads(request.body)
    try:
        commande_produit = commande.commande_produits.get(produit=body.get('produit_id'))
    except CommandeProduit.DoesNotExist:
        produit = Produit.objects.get(id=body.get('produit_id'))
        commande_produit = CommandeProduit.objects.create(produit=produit, commande=commande)
    commande_produit.quantite = body.get('quantite')
    commande_produit.save()
    return JsonResponse({
        'commande': commande.to_json(),
    })


def commande_detail(request):
    uuid = request.COOKIES.get('commande_uuid')
    try:
        commande = Commande.objects.get(uuid=uuid)
    except Commande.DoesNotExist:
        commande = Commande.objects.create()
    reponse = JsonResponse({
        'commande': commande.to_json(),
    })
    reponse.set_cookie('commande_uuid', commande.uuid, max_age=None, samesite='Strict')
    return reponse


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

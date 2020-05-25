import json
from functools import reduce

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse

from .models import Categorie, Produit, Commande, CommandeProduit, CommandeForm


def commande_ajouter(request):
    """Fonction principale qui permet de modifier la quantité d'un produit dans le panier.
    Il faut toujours passer par cette fonction afin de calculer correctement les prix.
    """
    uuid = request.COOKIES.get('commande_uuid')
    commande = Commande.objects.get(uuid=uuid)
    if commande.est_validee:
        raise Exception('La commande a déjà été validée.')
    body = json.loads(request.body)
    try:
        commande_produit = commande.commande_produits.get(produit=body.get('produit_id'))
        produit = commande_produit.produit
    except CommandeProduit.DoesNotExist:
        produit = Produit.objects.get(id=body.get('produit_id'))
        commande_produit = CommandeProduit.objects.create(produit=produit, commande=commande)
    commande_produit.quantite = body.get('quantite', 0)
    commande_produit.prix_unitaire = produit.prix
    commande_produit.prix_total = produit.prix * commande_produit.quantite
    commande_produit.save()
    commande.prix_total = reduce(
        (lambda total, commande_produit: total + commande_produit.prix_total),
        commande.commande_produits.all(),
        0
    )
    commande.save()
    return JsonResponse({
        'commande': commande.to_json(),
    })


def commande_detail(request):
    uuid = request.COOKIES.get('commande_uuid')
    try:
        commande = Commande.objects.get(uuid=uuid)
    except (Commande.DoesNotExist, ValidationError):
        commande = Commande.objects.create()
    reponse = JsonResponse({
        'commande': commande.to_json(),
    })
    reponse.set_cookie('commande_uuid', commande.uuid, max_age=None, samesite='Strict')
    return reponse


def commande_finaliser(request):
    uuid = request.COOKIES.get('commande_uuid')
    try:
        commande = Commande.objects.get(uuid=uuid)
    except Commande.DoesNotExist:
        commande = Commande.objects.create()

    if request.method == "POST" and not commande.est_validee:
        commande_form = CommandeForm(request.POST, instance=commande)
        if commande_form.is_valid():
            commande = commande_form.save(commit=False)
            commande.est_validee = True
            commande.save()
            # TODO envoyer email
    else:
        commande_form = CommandeForm(instance=commande)

    reponse = render(request, 'commande_finaliser.html', {
        'commande': commande,
        'commande_form': commande_form,
        'commande_produits': commande.commande_produits.filter(quantite__gt=0),
    })

    if commande.est_validee:
        # commence un nouveau panier
        reponse.delete_cookie('commande_uuid')

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

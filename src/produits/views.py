import json
from functools import reduce

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse

from .models import Categorie, Produit, Commande, CommandeProduit, CommandeForm, ProduitAttributValeur


def commande_ajouter(request):
    """Fonction principale qui permet de modifier la quantité d'un produit dans le panier.
    Il faut toujours passer par cette fonction afin de calculer correctement les prix.
    """
    uuid = request.COOKIES.get('commande_uuid')
    commande = Commande.objects.get(uuid=uuid)
    if commande.est_validee:
        raise Exception('La commande a déjà été validée.')
    body = json.loads(request.body)
    produit = Produit.objects.get(id=body.get('produit_id'))
    valeur_ids = body.get('valeur_ids', [])

    # on s'assure que les valeurs reçues correspondant à une combinaison de valeur autorisée sur le produit
    if produit.validation_valeurs(valeur_ids):
        produit_attribut_valeurs = [
            ProduitAttributValeur.objects.get(id=valeur_id)
            for valeur_id in valeur_ids
        ]
    else:
        # sinon on utilise la première combinaison possible
        produit_attribut_valeurs = produit.premiere_combinaison_valeurs()

    try:
        # récupère tous les CommandeProduit associé au produit reçu
        commande_produits = commande.commande_produits.filter(produit=produit.id)
        commande_produit = False
        # essaye de trouver quel CommandeProduit correspond aux valeurs reçues
        for commande_produit_tmp in commande_produits:
            if commande_produit_tmp.contient_valeurs(produit_attribut_valeurs):
                commande_produit = commande_produit_tmp
                break
        if not commande_produit:
            raise CommandeProduit.DoesNotExist
    except CommandeProduit.DoesNotExist:
        # si aucun CommandeProduit ne correspond, on le crée
        commande_produit = CommandeProduit.objects.create(produit=produit, commande=commande)
        commande_produit.produit_attribut_valeurs.set(produit_attribut_valeurs)

    # mise à jour de la quantité et calcul des prix du produit
    commande_produit.quantite = body.get('quantite', 0)
    commande_produit.prix_unitaire = produit.prix + sum(pav.prix_extra for pav in commande_produit.produit_attribut_valeurs.all())
    commande_produit.prix_total = commande_produit.prix_unitaire * commande_produit.quantite
    commande_produit.save()

    # recalcul du prix total
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
        'commande_produits': commande.commande_produits.exclude(quantite=0),
    })

    if commande.est_validee:
        # commence un nouveau panier
        reponse.delete_cookie('commande_uuid')

    return reponse


def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'categories.html', {
        'categories': categories,
    })


def categorie(request, categorie_id):
    categorie = Categorie.objects.get(id=categorie_id)
    produits = categorie.produits.filter(en_vente=True).order_by('-special', 'ordre_tri', 'id')
    return render(request, 'produits.html', {
        'categorie': categorie,
        'produits': produits,
    })

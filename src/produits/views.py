import json

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse

from .models import Categorie, Commande, CommandeForm


def commande_ajouter(request):
    uuid = request.COOKIES.get('commande_uuid')
    commande = Commande.objects.get(uuid=uuid)
    body = json.loads(request.body)

    commande.ajouter_ou_modifier_produit(
        body.get('produit_id'),
        body.get('valeur_ids', []),
        body.get('quantite', 0)
    )

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

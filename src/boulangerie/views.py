import random
from django.shortcuts import render


def produits(request):
    return render(request, 'produits.html')


def contact(request):
    return render(request, 'contact.html')


def commande(request):
    return render(request, 'commande.html')


def sandwich(request):
    return render(request, 'Sandwich.html')

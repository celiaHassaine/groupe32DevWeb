import random

from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil.html')

def produits(request):
	return render(request, 'produits.html')

def contact(request):
	return render(request, 'accueil.html')

def commande(request):
	return render(request, 'commande.html')
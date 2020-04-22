import random

from django.shortcuts import render

def accueil(request):
	# TODO replacer par un SELECT dans la table actualite
	params = {
		'actualites': [
			{
				'titre':  "Actu 1: super tarte",
			},
			{
				'titre':  "Actu 2: nouveau sandwich",
				'contenu': "super bon",
			}
		],
	}
	return render(request, 'accueil.html', params)

def produits(request):
	return render(request, 'produits.html')

def contact(request):
	return render(request, 'contact.html')

def commande(request):
	return render(request, 'commande.html')
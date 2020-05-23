import random
from django.shortcuts import render


def commande(request):
    return render(request, 'commande.html')



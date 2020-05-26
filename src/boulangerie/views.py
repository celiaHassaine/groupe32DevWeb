from django.shortcuts import render


def commande(request):
    return render(request, 'commande.html')


def contact(request):
    return render(request, 'contact.html')

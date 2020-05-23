from django.shortcuts import render
from .models import News
from django.apps import apps

Categorie = apps.get_model('produits', 'Categorie')


def accueil(request):
    categories = Categorie.objects.all()
    actualites = News.objects.order_by('-id')[:3]
    return render(request, 'accueil.html', {
        'actualites': actualites,
        'categories': categories,
    })

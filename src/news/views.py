import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import News
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings


# Create your views here.

def listing(request):
    news = News.objects.all()
    formated_news = [
        "<li><img src=\"{}\" alt=\"{}\"><br/>{}<br/>{}</li>".format(album.img.url, album.titre, album.titre,
                                                                    album.contenu) for album in news]
    message = """<ul>{}</ul>""".format("\n".join(formated_news))
    return HttpResponse(message)


def listingsansimg(request):
    news = News.objects.all()
    formated_news = ["<li>{}<br/>{}</li>".format(album.titre, album.contenu) for album in news]
    message = """<ul>{}</ul>""".format("\n".join(formated_news))
    return HttpResponse(message)


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = News.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        albums = News.objects.filter(titre__icontains=query)

    if not albums.exists():
        message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    else:
        albums = ["<li><img src=\"{}\" alt=\"{}\"><br/>{}<br/>{}</li>".format(album.img.url, album.titre, album.titre,
                                                                              album.contenu) for album in albums]
        message = """
            Nous avons trouvé les articles correspondant à votre requête ! Les voici :
            <ul>{}</ul>
        """.format("</li><li>".join(albums))

    return HttpResponse(message)


def accueil(request):
    actualites = News.objects.order_by('-id')[:3]
    return render(request, 'accueil.html', {
        'actualites' : actualites,
    })

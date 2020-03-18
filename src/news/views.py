from django.shortcuts import render
from django.http import HttpResponse
from .models import News

# Create your views here.

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def listing(request):
    news = News.objects.all()
    formated_news = ["<li>{}</li>".format(new.titre) for new in news]
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
        albums = ["<li>{}</li>".format(album.titre) for album in albums]
        message = """
            Nous avons trouvé les articles correspondant à votre requête ! Les voici :
            <ul>{}</ul>
        """.format("</li><li>".join(albums))

    return HttpResponse(message)

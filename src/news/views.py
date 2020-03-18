#from django.shortcuts import render
from django.http import HttpResponse
from .models import News

# Create your views here.

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def listing(request):
    news = News.objects
    formated_news = ["<li>{}</li>".format(new['titre']) for new in news]
    message = """<ul>{}</ul>""".format("\n".join(formated_news))
    return HttpResponse(message)


#from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def listing(request):
    news = ["<li>{}</li>".format(news['titre']) for news in News]
    message = """<ul>{}</ul>""".format("\n".join(news))
    return HttpResponse(message)


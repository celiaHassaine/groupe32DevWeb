from django.db import models


# Create your models here.

class News(models.Model):
    titre = models.CharField(max_length=100)
    contenu = models.TextField()


class Fichier(models.Model):
    chemin = models.URLField()
    nom = models.CharField(max_length=100)
    news = models.ForeignKey(News, on_delete=models.CASCADE())

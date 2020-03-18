from django.db import models


# Create your models here.

class News(models.Model):
    titre = models.CharField(max_length=100)
    contenu = models.TextField()
    img = models.ImageField(upload_to='pics', default = 'pics/no-img.jpg')  # pics sera le nom du dossier ou on cherchera les photos
    def __str__(self):
        return self.titre

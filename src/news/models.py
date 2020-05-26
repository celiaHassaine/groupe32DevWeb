from django.db import models
from django.conf import settings


class News(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    contenu = models.TextField()
    img = models.ImageField(upload_to='news', blank=True)

    def __str__(self):
        return self.titre

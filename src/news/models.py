from django.db import models
from django.conf import settings
from django.urls import reverse

# BONUS django hosts ---> subdomain name for reverse (MIEUX POUR REVERSE)

from rest_framework.reverse import reverse as api_reverse


# Create your models here.

class News(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    contenu = models.TextField()
    img = models.ImageField(upload_to='pics',
                            default='pics/no-img.jpg')  # pics sera le nom du dossier ou on cherchera les photos

    def __str__(self):
        return self.titre

    @property
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        return api_reverse("api-news:post-rud", kwargs={'pk': self.pk}, request=request)

# Create your models here.
import uuid

from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.forms import ModelForm, DateInput

from rest_framework.reverse import reverse as api_reverse


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField('categorie', blank=True)
    ordre_tri = models.IntegerField()

    def __str__(self):
        return self.nom

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-cat", kwargs={'pk': self.pk}, request=request)


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    categorie = models.ForeignKey('Categorie', PROTECT, related_name='produits')
    special = models.BooleanField(default=False)
    en_vente = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    ordre_tri = models.IntegerField(default=10)
    image = models.ImageField('produit', blank=True)

    def __str__(self):
        return self.nom

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-prod", kwargs={'pk': self.pk}, request=request)


class Attribut(models.Model):
    nom = models.CharField(max_length=100)
    produits = models.ManyToManyField('Produit', through='ProduitAttribut')

    def __str__(self):
        return self.nom

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-attr", kwargs={'pk': self.pk}, request=request)


class Valeur(models.Model):
    attribut = models.ForeignKey('Attribut', CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return '%s: %s' % (self.attribut, self.nom)

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-val", kwargs={'pk': self.pk}, request=request)


class ProduitAttribut(models.Model):
    produit = models.ForeignKey('Produit', CASCADE, related_name='produit_attributs')
    attribut = models.ForeignKey('Attribut', CASCADE)

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-prodattr", kwargs={'pk': self.pk}, request=request)


class ProduitAttributValeur(models.Model):
    produit_attribut = models.ForeignKey('ProduitAttribut', CASCADE, related_name='produit_attribut_valeurs')
    valeur = models.ForeignKey('Valeur', CASCADE)

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-pav", kwargs={'pk': self.pk}, request=request)


class Commande(models.Model):
    nom_client = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    prix_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_recuperation = models.DateField(null=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    est_validee = models.BooleanField(default=False)

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-comm", kwargs={'pk': self.pk}, request=request)

    def to_json(self):
        return {
            'id': self.id,
            'produits': [{
                'id': commande_produit.produit.id,
                'nom': commande_produit.produit.nom,
                'image': commande_produit.produit.image.url if commande_produit.produit.image else False,
                'prix_unitaire': commande_produit.prix_unitaire,
                'prix_total': commande_produit.prix_total,
                'quantite': commande_produit.quantite,
            } for commande_produit in self.commande_produits.all()],
            'prix_total': self.prix_total,
        }


class CommandeProduit(models.Model):
    commande = models.ForeignKey('Commande', CASCADE, related_name='commande_produits')
    produit = models.ForeignKey('Produit', PROTECT)
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    prix_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def get_api_url(self, request=None):
        return api_reverse("api-produits:post-rud-commprod", kwargs={'pk': self.pk}, request=request)


class CommandeForm(ModelForm):
    class Meta:
        model = Commande
        fields = ['nom_client', 'telephone', 'date_recuperation']
        widgets = {
            'date_recuperation': DateInput(attrs={'type': 'date'})
        }

# Create your models here.

from django.db import models
from django.db.models.deletion import CASCADE, PROTECT


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField('categorie', blank=True)
    ordre_tri = models.IntegerField()

    def __str__(self):
        return self.nom


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


class Attribut(models.Model):
    nom = models.CharField(max_length=100)
    produits = models.ManyToManyField('Produit', through='ProduitAttribut')

    def __str__(self):
        return self.nom


class Valeur(models.Model):
    attribut = models.ForeignKey('Attribut', CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return '%s: %s' % (self.attribut, self.nom)


class ProduitAttribut(models.Model):
    produit = models.ForeignKey('Produit', CASCADE, related_name='produit_attributs')
    attribut = models.ForeignKey('Attribut', CASCADE)


class ProduitAttributValeur(models.Model):
    produit_attribut = models.ForeignKey('ProduitAttribut', CASCADE, related_name='produit_attribut_valeurs')
    valeur = models.ForeignKey('Valeur', CASCADE)


class Commande(models.Model):
    nom_client = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    prix_total = models.DecimalField(max_digits=5, decimal_places=2)


class CommandeProduit(models.Model):
    commande = models.ForeignKey('Commande', CASCADE)
    produit = models.ForeignKey('Produit', PROTECT)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=5, decimal_places=2)
    prix_total = models.DecimalField(max_digits=5, decimal_places=2)

# Create your models here.

from django.db import models

CATEGORY_CHOICES = (
    ('B', 'Boulangerie'),
    ('FB', 'Fine Boulangerie'),
    ('PAI', 'Pain'),
    ('PAT', 'Patisserie'),
    ('T', 'Tarte'),
)

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categorie', blank=True)
    ordre_tri = models.IntegerField()

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    categorie = models.ForeignKey(to='Categorie', on_delete=models.PROTECT, related_name='produits')
    special = models.BooleanField(default=False)
    en_vente = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    ordreTri = models.IntegerField()
    image = models.ImageField(upload_to='pics', default='pics/no-img.jpg')

    def __str__(self):
        return self.nom


class Attribut(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
    idProd = models.ManyToManyField(Produit, through='ProdAttr')


class ProdAttr(models.Model):
    idProduit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    idAttr = models.ForeignKey(Attribut, on_delete=models.CASCADE)


class Valeur(models.Model):
    nom = models.CharField(max_length=100)
    idAttr = models.ForeignKey(ProdAttr, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Commandes(models.Model):
    nomCLient = models.CharField(max_length=50)
    prenomClient = models.CharField(max_length=50)
    telephone = models.IntegerField()
    prixCommande = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nomCLient
    idProduits = models.ManyToManyField(Produit, through='CommProd')


class CommProd(models.Model):
    idProduits = models.ForeignKey(Produit, on_delete=models.CASCADE)
    idCommande = models.ForeignKey(Commandes, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prixUnitaire = models.DecimalField(max_digits=5, decimal_places=2)
    prixLigne = models.DecimalField(max_digits=5, decimal_places=2)

"""class ProdAttrValeur(models.Model):
    idValeur = models.ForeignKey(Valeur)
    idProdAttr = models.ForeignKey(ProdAttr)
"""

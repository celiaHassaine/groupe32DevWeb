# Create your models here.

from django.db import models

CATEGORY_CHOICES = (
    ('B', 'Boulangerie'),
    ('FB', 'Fine Boulangerie'),
    ('PAI', 'Pain'),
    ('PAT', 'Patisserie'),
    ('T', 'Tarte'),
)


class Produits(models.Model):
    nomProduits = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    categorie = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    special = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)
    description = models.CharField(max_length=150)
    ordreTri = models.IntegerField()
    image = models.ImageField(upload_to='pics',
                              default='pics/no-img.jpg')

    def __str__(self):
        return self.nomProduits


class Attribut(models.Model):
    nom = models.CharField(max_length=100)
    idProd = models.ManyToManyField(Produits, through='ProdAttr')

    def __str__(self):
        return self.nom


class ProdAttr(models.Model):
    idProduit = models.ForeignKey(Produits, on_delete=models.CASCADE)
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
    idProduits = models.ManyToManyField(Produits, through='CommProd')

    def __str__(self):
        return self.nomCLient


class CommProd(models.Model):
    idProduits = models.ForeignKey(Produits, on_delete=models.CASCADE)
    idCommande = models.ForeignKey(Commandes, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prixUnitaire = models.DecimalField(max_digits=5, decimal_places=2)
    prixLigne = models.DecimalField(max_digits=5, decimal_places=2)


"""class ProdAttrValeur(models.Model):
    idValeur = models.ForeignKey(Valeur)
    idProdAttr = models.ForeignKey(ProdAttr)
"""

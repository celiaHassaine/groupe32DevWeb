# Create your models here.
import uuid

from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.forms import ModelForm, DateInput


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

    def validation_valeurs(self, valeur_ids):
        """Chaque produit possède une ou plusieurs combinaisons d'attribut et de valeurs possibles.
        Le but de cette méthode est de s'assurer que les valeurs reçues en paramètre correspondent
        exactement à une combinaison possible du produit."""
        for produit_attribut in self.produit_attributs.all():
            attribut_ok = False
            for produit_attribut_valeur in produit_attribut.produit_attribut_valeurs.all():
                if produit_attribut_valeur.id in valeur_ids:
                    if not attribut_ok:
                        attribut_ok = True
                    else:
                        # il est interdit de prendre plusieurs valeurs pour le même attribut
                        return False
            if not attribut_ok:
                # aucune valeur n'a été trouvée pour un attribut
                return False
        return True

    def premiere_combinaison_valeurs(self):
        """Retourne la première combinaison de valeur possible pour ce produit,
        ce qui revient à prendre la première valeure possible de chaque attribut."""
        produit_attribut_valeurs = []
        for produit_attribut in self.produit_attributs.all():
            for produit_attribut_valeur in produit_attribut.produit_attribut_valeurs.all():
                produit_attribut_valeurs.append(produit_attribut_valeur)
                break
        return produit_attribut_valeurs

    def produit_attributs_avec_choix(self):
        return [pa for pa in self.produit_attributs.all() if len(pa.produit_attribut_valeurs.all()) != 1]

    def produit_attributs_sans_choix(self):
        return [pa for pa in self.produit_attributs.all() if len(pa.produit_attribut_valeurs.all()) == 1]


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
    prix_extra = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return '%s: %s' % (self.produit_attribut.produit, self.valeur)


class Commande(models.Model):
    nom_client = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    prix_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_recuperation = models.DateField(null=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    est_validee = models.BooleanField(default=False)

    def to_json(self):
        return {
            'id': self.id,
            'commande_produits': [{
                'id': commande_produit.id,
                'produit': {
                    'id': commande_produit.produit.id,
                    'nom': commande_produit.produit.nom,
                    'image': commande_produit.produit.image.url if commande_produit.produit.image else False,
                    'prix': commande_produit.produit.prix,
                    'produit_attributs': [{
                        'id': produit_attribut.id,
                        'nom': produit_attribut.attribut.nom,
                        'valeur_selectionee': commande_produit.produit_attribut_valeurs.get(produit_attribut=produit_attribut).id,
                        'produit_attribut_valeurs': [{
                            'id': produit_attribut_valeur.id,
                            'nom': produit_attribut_valeur.valeur.nom,
                            'prix_extra': produit_attribut_valeur.prix_extra,
                        } for produit_attribut_valeur in produit_attribut.produit_attribut_valeurs.all()],
                    } for produit_attribut in commande_produit.produit.produit_attributs.all()],
                },
                'prix_unitaire': commande_produit.prix_unitaire,
                'prix_total': commande_produit.prix_total,
                'quantite': commande_produit.quantite,
            } for commande_produit in self.commande_produits.all()],
            'prix_total': self.prix_total,
        }


class CommandeProduit(models.Model):
    commande = models.ForeignKey('Commande', CASCADE, related_name='commande_produits')
    produit = models.ForeignKey('Produit', PROTECT)
    produit_attribut_valeurs = models.ManyToManyField('ProduitAttributValeur')
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    prix_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def contient_valeurs(self, produit_attribut_valeurs):
        """Une commande peut contenir plusieurs fois le même produit mais avec des attributs et valeurs
        différentes. Le but de cette fonction est de retourner si le CommandeProduit actuel correspond
        à toutes les valeurs reçues."""
        valeur_ids = [v.id for v in produit_attribut_valeurs]
        self_valeur_ids = [v.id for v in self.produit_attribut_valeurs.all()]
        # toutes les valeurs reçus doivent présentes
        for valeur_id in valeur_ids:
            if valeur_id not in self_valeur_ids:
                return False
        # toutes les valeurs présentes doivent être reçues
        for valeur_id in self_valeur_ids:
            if valeur_id not in valeur_ids:
                return False
        return True


class CommandeForm(ModelForm):
    class Meta:
        model = Commande
        fields = ['nom_client', 'telephone', 'date_recuperation']
        widgets = {
            'date_recuperation': DateInput(attrs={'type': 'date'})
        }

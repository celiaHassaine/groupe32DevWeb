from decimal import Decimal

from django.test import TestCase

from .models import Attribut, Valeur, ProduitAttributValeur, Categorie, Commande, CommandeProduit, Produit, ProduitAttribut


class ProduitsCase(TestCase):
    def setUp(self):
        # categorie
        self.pain = Categorie.objects.create(nom="Pain")
        self.viennoiserie = Categorie.objects.create(nom="Viennoiserie")
        self.sandwich = Categorie.objects.create(nom="Sanwdich")

        # attributs & valeurs
        self.poids = Attribut.objects.create(nom="Poids")
        self.poids_400g = Valeur.objects.create(nom="400g", attribut=self.poids)
        self.poids_800g = Valeur.objects.create(nom="800g", attribut=self.poids)

        self.ingredient = Attribut.objects.create(nom="Ingrédient")
        self.jambon = Valeur.objects.create(nom="Jambon", attribut=self.ingredient)
        self.fromage = Valeur.objects.create(nom="Fromage", attribut=self.ingredient)

        # produits

        # produit avec choix
        self.pain_blanc = Produit.objects.create(nom="Pain blanc", prix=Decimal("1.5"), categorie=self.pain)
        self.pain_blanc_poids = ProduitAttribut.objects.create(produit=self.pain_blanc, attribut=self.poids)
        self.pain_blanc_poids_400g = ProduitAttributValeur.objects.create(produit_attribut=self.pain_blanc_poids, valeur=self.poids_400g)
        self.pain_blanc_poids_800g = ProduitAttributValeur.objects.create(produit_attribut=self.pain_blanc_poids, valeur=self.poids_800g, prix_extra=Decimal("1.2"))

        # produit sans attribut
        self.croissant = Produit.objects.create(nom="Croissant", prix=Decimal("1"), categorie=self.viennoiserie)

        # produit avec attribut sans choix
        self.club = Produit.objects.create(nom="Club", prix=Decimal("4.1"), categorie=self.sandwich)
        self.club_ingredient_1 = ProduitAttribut.objects.create(produit=self.club, attribut=self.ingredient)
        self.club_ingredient_1_jambon = ProduitAttributValeur.objects.create(produit_attribut=self.club_ingredient_1, valeur=self.jambon)
        self.club_ingredient_2 = ProduitAttribut.objects.create(produit=self.club, attribut=self.ingredient)
        self.club_ingredient_2_fromage = ProduitAttributValeur.objects.create(produit_attribut=self.club_ingredient_2, valeur=self.fromage)

    def test_categorie____str__(self):
        self.assertEqual(str(self.pain), "Pain")

    def test_produit____str__(self):
        self.assertEqual(str(self.pain_blanc), "Pain blanc")

    def test_attribut____str__(self):
        self.assertEqual(str(self.poids), "Poids")

    def test_valeur____str__(self):
        self.assertEqual(str(self.jambon), "Ingrédient: Jambon")

    def test_produit_attribut____str__(self):
        self.assertEqual(str(self.pain_blanc_poids), "Pain blanc: Poids")

    def test_produit_attribut_valeur____str__(self):
        self.assertEqual(str(self.pain_blanc_poids_400g), "Pain blanc: Poids: 400g")

    def test_produit__trouver_attribut_valeurs_possibles(self):
        # cas 1a: on passe des valeurs possibles (produit avec un attribut)
        produit_attribut_valeurs = self.pain_blanc.trouver_attribut_valeurs_possibles([self.pain_blanc_poids_400g.id])
        self.assertEqual(len(produit_attribut_valeurs), 1)
        self.assertEqual(produit_attribut_valeurs[0].id, self.pain_blanc_poids_400g.id)

        # cas 1b: on passe des valeurs possibles (produit sans attribut)
        produit_attribut_valeurs = self.croissant.trouver_attribut_valeurs_possibles([])
        self.assertEqual(len(produit_attribut_valeurs), 0)

        # cas 1c: on passe des valeurs possibles (produit avec multiple attributs)
        produit_attribut_valeurs = self.club.trouver_attribut_valeurs_possibles([self.club_ingredient_1_jambon.id, self.club_ingredient_2_fromage.id])
        self.assertEqual(len(produit_attribut_valeurs), 2)
        self.assertEqual(produit_attribut_valeurs[0].id, self.club_ingredient_1_jambon.id)
        self.assertEqual(produit_attribut_valeurs[1].id, self.club_ingredient_2_fromage.id)

        # cas 2a: on passe des valeurs incorrectes, retour de la premère combinaison correcte
        produit_attribut_valeurs = self.pain_blanc.trouver_attribut_valeurs_possibles([self.club_ingredient_1_jambon.id])
        self.assertEqual(len(produit_attribut_valeurs), 1)
        self.assertEqual(produit_attribut_valeurs[0].id, self.pain_blanc_poids_400g.id)

        # cas 2b: on passe des valeurs incorrectes (pas assez de valeurs), retour de la premère combinaison correcte
        produit_attribut_valeurs = self.pain_blanc.trouver_attribut_valeurs_possibles([])
        self.assertEqual(len(produit_attribut_valeurs), 1)
        self.assertEqual(produit_attribut_valeurs[0].id, self.pain_blanc_poids_400g.id)

        # cas 2c: on passe des valeurs incorrectes (trop de valeurs), retour de la premère combinaison correcte
        produit_attribut_valeurs = self.pain_blanc.trouver_attribut_valeurs_possibles([self.pain_blanc_poids_400g.id, self.pain_blanc_poids_800g.id])
        self.assertEqual(len(produit_attribut_valeurs), 1)
        self.assertEqual(produit_attribut_valeurs[0].id, self.pain_blanc_poids_400g.id)

    def test_produit__validation_valeurs(self):
        # cas 1a: on passe des valeurs possibles (produit avec un attribut)
        valide = self.pain_blanc.validation_valeurs([self.pain_blanc_poids_400g.id])
        self.assertTrue(valide)

        # cas 1b: on passe des valeurs possibles (produit sans attribut)
        valide = self.croissant.validation_valeurs([])
        self.assertTrue(valide)

        # cas 1c: on passe des valeurs possibles (produit avec multiple attributs)
        valide = self.club.validation_valeurs([self.club_ingredient_1_jambon.id, self.club_ingredient_2_fromage.id])
        self.assertTrue(valide)

        # cas 2a: on passe des valeurs incorrectes
        valide = self.pain_blanc.validation_valeurs([self.club_ingredient_1_jambon.id])
        self.assertFalse(valide)

        # cas 2b: on passe des valeurs incorrectes (pas assez de valeurs)
        valide = self.pain_blanc.validation_valeurs([])
        self.assertFalse(valide)

        # cas 2c: on passe des valeurs incorrectes (trop de valeurs)
        valide = self.pain_blanc.validation_valeurs([self.pain_blanc_poids_400g.id, self.pain_blanc_poids_800g.id])
        self.assertFalse(valide)

    def test_produit__premiere_combinaison_valeurs(self):
        # cas 1: 1 attribut, plusieurs valeurs possibles
        produit_attribut_valeurs = self.pain_blanc.premiere_combinaison_valeurs()
        self.assertEqual(len(produit_attribut_valeurs), 1)
        self.assertEqual(produit_attribut_valeurs[0].id, self.pain_blanc_poids_400g.id)

        # cas 2: pas d'attribut
        produit_attribut_valeurs = self.croissant.premiere_combinaison_valeurs()
        self.assertEqual(len(produit_attribut_valeurs), 0)

        # cas 3: plusieurs attributs
        produit_attribut_valeurs = self.club.premiere_combinaison_valeurs()
        self.assertEqual(len(produit_attribut_valeurs), 2)
        self.assertEqual(produit_attribut_valeurs[0].id, self.club_ingredient_1_jambon.id)
        self.assertEqual(produit_attribut_valeurs[1].id, self.club_ingredient_2_fromage.id)

    def test_produit__produit_attributs_avec_choix(self):
        # cas 1: choix
        produit_attributs = self.pain_blanc.produit_attributs_avec_choix()
        self.assertEqual(len(produit_attributs), 1)
        self.assertEqual(produit_attributs[0].id, self.pain_blanc_poids.id)

        # cas 2: pas de choix
        produit_attributs = self.club.produit_attributs_avec_choix()
        self.assertEqual(len(produit_attributs), 0)

    def test_produit__produit_attributs_sans_choix(self):
        # cas 1: pas de sans choix
        produit_attributs = self.pain_blanc.produit_attributs_sans_choix()
        self.assertEqual(len(produit_attributs), 0)

        # cas 2: tous sans choix
        produit_attributs = self.club.produit_attributs_sans_choix()
        self.assertEqual(len(produit_attributs), 2)
        self.assertEqual(produit_attributs[0].id, self.club_ingredient_1.id)
        self.assertEqual(produit_attributs[1].id, self.club_ingredient_2.id)

    def test_commande__ajouter_ou_modifier_produit(self):
        # cas 1: commande déjà validée
        commande = Commande.objects.create(est_validee=True)
        with self.assertRaises(Exception):
            commande.ajouter_ou_modifier_produit(self.pain_blanc.id, [self.pain_blanc_poids_400g.id], 1)

        # cas 2: commande non validée, mise à jour possible
        commande = Commande.objects.create()
        commande.ajouter_ou_modifier_produit(self.pain_blanc.id, [self.pain_blanc_poids_400g.id], 1)
        commande_produits = commande.commande_produits.all()
        self.assertEqual(len(commande_produits), 1)
        self.assertEqual(commande_produits[0].produit.id, self.pain_blanc.id)
        self.assertEqual(commande_produits[0].quantite, 1)
        self.assertEqual(commande_produits[0].prix_unitaire, self.pain_blanc.prix)
        self.assertEqual(commande_produits[0].prix_total, self.pain_blanc.prix)
        self.assertEqual(commande.prix_total, self.pain_blanc.prix)
        self.assertEqual(self.pain_blanc.prix, Decimal("1.5"))

    def test_commande__trouver_commande_produit(self):
        # cas 1: le produit existe déjà dans la commande
        commande = Commande.objects.create()
        commande_pain_blanc_800g = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc)
        commande_pain_blanc_800g.produit_attribut_valeurs.set([self.pain_blanc_poids_800g])
        commande_produit = commande.trouver_commande_produit(self.pain_blanc, [self.pain_blanc_poids_800g])
        self.assertEqual(commande_pain_blanc_800g.id, commande_produit.id)

        # cas 2: le produit n'existe pas encore dans la commande
        commande = Commande.objects.create()
        commande_produit = commande.trouver_commande_produit(self.pain_blanc, [self.pain_blanc_poids_800g])
        self.assertTrue(commande_produit)
        self.assertEqual(commande_produit.produit.id, self.pain_blanc.id)
        produit_attribut_valeurs = commande_produit.produit_attribut_valeurs.all()
        self.assertEqual(len(produit_attribut_valeurs), 1)
        self.assertEqual(produit_attribut_valeurs[0].id, self.pain_blanc_poids_800g.id)

        # cas 3: le produit existe déjà dans la commande mais avec d'autres valeurs
        commande = Commande.objects.create()
        commande_pain_blanc_800g = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc)
        commande_pain_blanc_800g.produit_attribut_valeurs.set([self.pain_blanc_poids_800g])
        commande_produit = commande.trouver_commande_produit(self.pain_blanc, [self.pain_blanc_poids_400g])
        self.assertTrue(commande_produit)
        self.assertTrue(commande_produit.id != commande_pain_blanc_800g.id)
        self.assertEqual(commande_produit.produit.id, self.pain_blanc.id)
        produit_attribut_valeurs = commande_produit.produit_attribut_valeurs.all()
        self.assertEqual(len(produit_attribut_valeurs), 1)
        self.assertEqual(produit_attribut_valeurs[0].id, self.pain_blanc_poids_400g.id)

    def test_commande__calcul_prix_total(self):
        # somme des prix des produits choisis
        commande = Commande.objects.create()
        commande_produit_1 = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc, prix_total=Decimal("2"))
        commande_produit_2 = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc, prix_total=Decimal("5"))
        commande.calcul_prix_total()
        self.assertEqual(commande.prix_total, commande_produit_1.prix_total + commande_produit_2.prix_total)
        self.assertEqual(commande.prix_total, Decimal("7"))

    def test_commande__to_json(self):
        commande = Commande.objects.create()
        commande.ajouter_ou_modifier_produit(self.pain_blanc.id, [self.pain_blanc_poids_400g.id], 1)
        # vérifie que la méthode ne crash pas
        data = commande.to_json()
        self.assertEqual(data['id'], commande.id)

    def test_commande_produit__contient_valeurs(self):
        commande = Commande.objects.create()
        # cas 1a: contient toutes les valeurs (une)
        commande_pain_blanc_800g = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc)
        commande_pain_blanc_800g.produit_attribut_valeurs.set([self.pain_blanc_poids_800g])
        contient = commande_pain_blanc_800g.contient_valeurs([self.pain_blanc_poids_800g])
        self.assertTrue(contient)

        # cas 1b: contient toutes les valeurs (plusieurs)
        commande_club = CommandeProduit.objects.create(commande=commande, produit=self.club)
        commande_club.produit_attribut_valeurs.set([self.club_ingredient_1_jambon, self.club_ingredient_2_fromage])
        contient = commande_club.contient_valeurs([self.club_ingredient_1_jambon, self.club_ingredient_2_fromage])
        self.assertTrue(contient)

        # cas 1c: pas besoin de valeur
        commande_croissant = CommandeProduit.objects.create(commande=commande, produit=self.croissant)
        contient = commande_croissant.contient_valeurs([])
        self.assertTrue(contient)

        # cas 2a: contient des valeurs invalides
        contient = commande_pain_blanc_800g.contient_valeurs([self.pain_blanc_poids_400g])
        self.assertFalse(contient)
        contient = commande_pain_blanc_800g.contient_valeurs([self.club_ingredient_2_fromage])
        self.assertFalse(contient)

        # cas 2b: contient trop de valeurs
        contient = commande_pain_blanc_800g.contient_valeurs([self.pain_blanc_poids_400g, self.pain_blanc_poids_800g])
        self.assertFalse(contient)

        # cas 2c: ne contient pas assez de valeurs
        contient = commande_pain_blanc_800g.contient_valeurs([])
        self.assertFalse(contient)
        contient = commande_club.contient_valeurs([self.club_ingredient_2_fromage])
        self.assertFalse(contient)

    def test_commande_produit__calcul_prix(self):
        commande = Commande.objects.create()
        # cas 1: quantité 1
        commande_pain_blanc_400g = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc, quantite=1)
        commande_pain_blanc_400g.produit_attribut_valeurs.set([self.pain_blanc_poids_400g])
        commande_pain_blanc_400g.calcul_prix()
        self.assertEqual(commande_pain_blanc_400g.prix_unitaire, self.pain_blanc.prix)
        self.assertEqual(commande_pain_blanc_400g.prix_total, self.pain_blanc.prix)
        self.assertEqual(commande_pain_blanc_400g.prix_total, Decimal("1.5"))

        # cas 2: quantité plusieurs
        commande_pain_blanc_400g = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc, quantite=3)
        commande_pain_blanc_400g.produit_attribut_valeurs.set([self.pain_blanc_poids_400g])
        commande_pain_blanc_400g.calcul_prix()
        self.assertEqual(commande_pain_blanc_400g.prix_unitaire, self.pain_blanc.prix)
        self.assertEqual(commande_pain_blanc_400g.prix_total, 3 * self.pain_blanc.prix)
        self.assertEqual(commande_pain_blanc_400g.prix_total, Decimal("4.5"))

        # cas 3: avec extra
        commande_pain_blanc_800g = CommandeProduit.objects.create(commande=commande, produit=self.pain_blanc, quantite=5)
        commande_pain_blanc_800g.produit_attribut_valeurs.set([self.pain_blanc_poids_800g])
        commande_pain_blanc_800g.calcul_prix()
        self.assertEqual(commande_pain_blanc_800g.prix_unitaire, self.pain_blanc.prix + self.pain_blanc_poids_800g.prix_extra)
        self.assertEqual(commande_pain_blanc_800g.prix_unitaire, Decimal("2.7"))
        self.assertEqual(commande_pain_blanc_800g.prix_total, (self.pain_blanc.prix + self.pain_blanc_poids_800g.prix_extra) * 5)
        self.assertEqual(commande_pain_blanc_800g.prix_total, Decimal("13.5"))

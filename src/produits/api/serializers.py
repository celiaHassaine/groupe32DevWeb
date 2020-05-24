from rest_framework import serializers
from produits.models import Categorie, Produit, Attribut, Valeur, ProduitAttribut, ProduitAttributValeur, Commande, \
    CommandeProduit


class CategorieSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Categorie
        fields = [
            'url',
            'id',
            'nom',
            'description',
            'image',
            'ordre_tri',
        ]
        read_only_fields = ['id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur
        # lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    # Serializer does 2 things:
    # converts to JSON and validations for data passed


class ProduitSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Produit
        fields = [
            'url',
            'id',
            'nom',
            'prix',
            'categorie',
            'special',
            'en_vente',
            'description',
            'ordre_tri',
            'image',
        ]
        read_only_fields = [
            'id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class AttributSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attribut
        fields = [
            'url',
            'id',
            'nom',
            'produits',
        ]
        read_only_fields = [
            'id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class ValeurSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Valeur
        fields = [
            'url',
            'id',
            'attribut',
            'nom',
        ]
        read_only_fields = [
            'id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class ProduitAttributSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProduitAttribut
        fields = [
            'url',
            'id',
            'produit',
            'attribut',
        ]
        read_only_fields = [
            'id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class ProduitAttributValeurSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProduitAttributValeur
        fields = [
            'url',
            'id',
            'produit_attribut',
            'valeur',
        ]
        read_only_fields = [
            'id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class CommandeSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Commande
        fields = [
            'url',
            'id',
            'nom_client',
            'telephone',
            'prix_total',
        ]
        read_only_fields = [
            'id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class CommandeProduitSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CommandeProduit
        fields = [
            'url',
            'id',
            'commande',
            'produit',
            'quantite',
            'prix_unitaire',
            'prix_total',
        ]
        read_only_fields = [
            'id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

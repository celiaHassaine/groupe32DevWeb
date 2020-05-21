from rest_framework import serializers
from contact.models import Adresse, Contact, Horaire


class AdresseSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Adresse
        fields = [
            'url',
            'id',
            'rue',
            'numero',
            'ville',
            'codePostale',
            'pays',
        ]
        read_only_fields = ['id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur
        # lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    """def validate_titre(self, value):
        qs = News.objects.filter(titre__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)  # pour éviter qu'il se compte lui-même
        if qs.exist():
            raise serializers.ValidationError("ce titre a déjà été utilisé")
        return value
        #Ca va mettre des conditions quand on entre des informations dans l api"""

    # Serializer does 2 things:
    # converts to JSON and validations for data passed


class ContactSerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Contact
        fields = [
            'url',
            'id',
            'telephone',
            'email',
            'adresse',
        ]
        read_only_fields = ['id']  # bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

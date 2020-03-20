from rest_framework import serializers
from news.models import News


class NewsSerializer(serializers.ModelSerializer):  # forms.ModelForm
    class Meta:
        model = News
        fields = [
            'pk',
            'user',
            'titre',
            'contenu',
            #'img',
        ]
        read_only_fields = ['user', 'pk'] #bon par exemple pour les données d utilisateur  (voir views pour traiter erreur lors d un post sans utilisateur

    def validate_titre(self, value):
        qs = News.objects.filter(titre__icontains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)  # pour éviter qu'il se compte lui-même
        if qs.exist():
            raise serializers.ValidationError("ce titre a déjà été utilisé")
        return value

    # Serializer does 2 things:
    # converts to JSON and validations for data passed

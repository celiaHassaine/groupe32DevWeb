# generic
from django.db.models import Q
from rest_framework import generics, mixins

from produits.models import Categorie, Produit, Attribut, Valeur, ProduitAttribut, ProduitAttributValeur, Commande, \
    CommandeProduit
from .permissions import IsOwnerOrReadOnly
from .serializers import CategorieSerializer, ProduitSerializer, AttributSerializer, ValeurSerializer, \
    ProduitAttributSerializer, ProduitAttributValeurSerializer, CommandeSerializer, CommandeProduitSerializer


class CategorieAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = CategorieSerializer

    def get_queryset(self):
        qss = Categorie.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class CategorieRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = CategorieSerializer
    #permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Categorie.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class ProduitAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ProduitSerializer

    def get_queryset(self):
        qss = Produit.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ProduitRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ProduitSerializer
    #permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Produit.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class AttributAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = AttributSerializer

    def get_queryset(self):
        qss = Attribut.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class AttributRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = AttributSerializer
    #permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Attribut.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class ValeurAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ValeurSerializer

    def get_queryset(self):
        qss = Valeur.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ValeurRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ValeurSerializer
    #permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Valeur.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class ProduitAttributAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ProduitAttributSerializer

    def get_queryset(self):
        qss = ProduitAttribut.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ProduitAttributRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ProduitAttributSerializer

    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return ProduitAttribut.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class ProduitAttributValeurAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'nom'  # (?P<pk>\d+) pk = id
    serializer_class = ProduitAttributValeurSerializer

    def get_queryset(self):
        qss = ProduitAttributValeur.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ProduitAttributValeurRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'nom'  # (?P<pk>\d+) pk = id
    serializer_class = ProduitAttributValeurSerializer

    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return ProduitAttributValeur.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class CommandeAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = CommandeSerializer

    def get_queryset(self):
        qss = Commande.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class CommandeRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = CommandeSerializer

    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Commande.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class CommandeProduitAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = CommandeProduitSerializer

    def get_queryset(self):
        qss = CommandeProduit.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save()  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class CommandeProduitRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = CommandeProduitSerializer

    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return CommandeProduit.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)

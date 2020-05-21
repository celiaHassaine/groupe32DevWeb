# generic
from django.db.models import Q
from rest_framework import generics, mixins

from contact.models import Adresse, Contact, Horaire
from .permissions import IsOwnerOrReadOnly
from .serializers import AdresseSerializer, ContactSerializer, HoraireSerializer


class AdresseAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = AdresseSerializer

    def get_queryset(self):
        qss = Adresse.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class AdresseRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = AdresseSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Adresse.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class ContactAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ContactSerializer

    def get_queryset(self):
        qss = Contact.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ContactRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = ContactSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Contact.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)


class HoraireAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = HoraireSerializer

    def get_queryset(self):
        qss = Horaire.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query) |
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class HoraireRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = HoraireSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Horaire.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)

# generic
from django.db.models import Q
from rest_framework import generics, mixins

from news.models import News
from .permissions import IsOwnerOrReadOnly
from .serializers import NewsSerializer


class NewsAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = NewsSerializer

    def get_queryset(self):
        qss = News.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qss = qss.filter(
                Q(titre__icontains=query)|
                Q(contenu__icontains=query)
            ).distinct()
        return qss

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Ceci servirait pour ce qui est dans read_only_fields

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class NewsRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview
    lookup_field = 'pk'  # (?P<pk>\d+) pk = id
    serializer_class = NewsSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return News.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #   pk = self.kwargs.get("pk")
    #  return News.objects.get(pk=pk)

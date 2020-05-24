from django.conf.urls import url

from .views import CategorieAPIView, CategorieRudView, \
    AttributAPIView, AttributRudView, \
    ValeurAPIView, ValeurRudView, \
    ProduitAPIView, ProduitRudView, \
    ProduitAttributAPIView, ProduitAttributRudView, \
    ProduitAttributValeurAPIView, ProduitAttributValeurRudView, \
    CommandeAPIView, CommandeRudView, \
    CommandeProduitAPIView, CommandeProduitRudView

urlpatterns = [
    url(r'^$', ProduitAPIView.as_view(), name='post-listcreate-prod'),
    url(r'^(?P<pk>\d+)/$', ProduitRudView.as_view(), name='post-rud-prod'),
    url(r'^categorie/$', CategorieAPIView.as_view(), name='post-listcreate-cat'),
    url(r'^categorie/(?P<pk>\d+)/$', CategorieRudView.as_view(), name='post-rud-cat'),
    url(r'^valeur/$', ValeurAPIView.as_view(), name='post-listcreate-val'),
    url(r'^valeur/(?P<pk>\d+)/$', ValeurRudView.as_view(), name='post-rud-val'),
    url(r'^attribut/$', AttributAPIView.as_view(), name='post-listcreate-attr'),
    url(r'^attribut/(?P<pk>\d+)/$', AttributRudView.as_view(), name='post-rud-attr'),
    url(r'^prodattr/$', ProduitAttributAPIView.as_view(), name='post-listcreate-prodattr'),
    url(r'^prodattr/(?P<pk>\d+)/$', ProduitAttributRudView.as_view(), name='post-rud-prodattr'),
    url(r'^pav/$', ProduitAttributValeurAPIView.as_view(), name='post-listcreate-pav'),
    url(r'^pav/(?P<pk>\d+)/$', ProduitAttributValeurRudView.as_view(), name='post-rud-pav'),
    url(r'^commande/$', CommandeAPIView.as_view(), name='post-listcreate-comm'),
    url(r'^commande/(?P<pk>\d+)/$', CommandeRudView.as_view(), name='post-rud-comm'),
    url(r'^comprod/$', CommandeProduitAPIView.as_view(), name='post-listcreate-comprod'),
    url(r'^comprod/(?P<pk>\d+)/$', CommandeProduitRudView.as_view(), name='post-rud-comprod'),
]

app_name = 'contact'

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
    url(r'^$', ProduitAPIView.as_view(), name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$', ProduitRudView.as_view(), name='post-rud'),
    url(r'^categorie/$', CategorieAPIView.as_view(), name='post-listcreate'),
    url(r'^categorie/(?P<pk>\d+)/$', CategorieRudView.as_view(), name='post-rud'),
    url(r'^valeur/$', ValeurAPIView.as_view(), name='post-listcreate'),
    url(r'^valeur/(?P<pk>\d+)/$', ValeurRudView.as_view(), name='post-rud'),
    url(r'^attribut/$', AttributAPIView.as_view(), name='post-listcreate'),
    url(r'^attribut/(?P<pk>\d+)/$', AttributRudView.as_view(), name='post-rud'),
    url(r'^prodattr/$', ProduitAttributAPIView.as_view(), name='post-listcreate'),
    url(r'^prodattr/(?P<pk>\d+)/$', ProduitAttributRudView.as_view(), name='post-rud'),
    url(r'^pav/$', ProduitAttributValeurAPIView.as_view(), name='post-listcreate'),
    url(r'^pav/(?P<pk>\d+)/$', ProduitAttributValeurRudView.as_view(), name='post-rud'),
    url(r'^commande/$', CommandeAPIView.as_view(), name='post-listcreate'),
    url(r'^commande/(?P<pk>\d+)/$', CommandeRudView.as_view(), name='post-rud'),
    url(r'^comprod/$', CommandeProduitAPIView.as_view(), name='post-listcreate'),
    url(r'^comprod/(?P<pk>\d+)/$', CommandeProduitRudView.as_view(), name='post-rud'),
]

app_name = 'contact'

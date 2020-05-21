from django.conf.urls import url

from .views import AdresseRudView, AdresseAPIView, ContactAPIView, ContactRudView, HoraireAPIView, HoraireRudView

urlpatterns = [
    url(r'^$', ContactAPIView.as_view(), name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$', ContactRudView.as_view(), name='post-rud'),
    url(r'^adresse/$', AdresseAPIView.as_view(), name='post-listcreate'),
    url(r'^adresse/(?P<pk>\d+)/$', AdresseRudView.as_view(), name='post-rud'),
    url(r'^horaire/$', HoraireAPIView.as_view(), name='post-listcreate'),
    url(r'^horaire/(?P<pk>\d+)/$', HoraireRudView.as_view(), name='post-rud'),
]

app_name = 'contact'

from django.conf.urls import url

from .views import AdresseRudView, AdresseAPIView, ContactAPIView, ContactRudView

urlpatterns = [
    url(r'^$', ContactAPIView.as_view(), name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$', ContactRudView.as_view(), name='post-rud'),
    url(r'^adresse/$', AdresseAPIView.as_view(), name='post-listcreate'),
    url(r'^adresse/(?P<pk>\d+)/$', AdresseRudView.as_view(), name='post-rud'),
]

app_name = 'contact'

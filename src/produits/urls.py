from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('liste/', views.listing, name='listing'),
    path('noimage/', views.listingsansimg, name='listingsansimg'),
    url(r'^search/$', views.search),
]
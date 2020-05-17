from django.conf.urls import url

from .views import NewsRudView, NewsAPIView

urlpatterns = [
    url(r'^$', NewsAPIView.as_view(), name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$', NewsRudView.as_view(), name='post-rud')
]

app_name = 'contact'

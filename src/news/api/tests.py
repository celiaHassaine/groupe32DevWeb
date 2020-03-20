from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

# automated
# new/ blank db --- on doit creer des données car la db est remise a zero
from rest_framework.reverse import reverse as api_reverse
from news.models import News

User = get_user_model()


class NewsAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test', email='test@test.com')
        user.set_password("random")
        user.save()
        news = News.objects.create(
            user=user,
            titre='new titre',
            contenu="fdsfdsq",
            img="pics/edward.jpg")

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = News.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api-news:post-listcreate")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

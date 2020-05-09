from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

# automated
# new/ blank db --- on doit creer des données car la db est remise a zero
from rest_framework.reverse import reverse as api_reverse
from news.models import News

User = get_user_model()


class NewsAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User.objects.create(username='test', email='test@test.com')
        user_obj.set_password("random")
        user_obj.save()
        news = News.objects.create(
            user=user_obj,
            titre='new titre',
            contenu="fdsfdsq", )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = News.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        # test the get list
        data = {}
        url = api_reverse("api-news:post-listcreate")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_post_item(self):
        # test the post
        data = {"titre": "nouveau", "contenu": "dsfsdcvs"}
        url = api_reverse("api-news:post-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        # test the get list
        news = News.objects.first()
        data = {}
        url = news.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_update_item(self):
        data = {"titre": "nouveau", "contenu": "dsfsdcvs"}
        news = News.objects.first()
        url = news.get_api_url()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        data = {"titre": "nouveau", "contenu": "dsfsdcvs"}
        news = News.objects.first()
        print(news.contenu)
        url = news.get_api_url()
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) #erreur a check
        print(response.data)

    def test_post_item_with_user(self):
        # test the post
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {"titre": "nouveau", "contenu": "dsfsdcvs"}
        url = api_reverse("api-news:post-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        # test the post
        owner = User.objects.create(username='testuser222')
        news = News.objects.create(
            user=owner,
            titre='new titre',
            contenu="fdsfdsq", )

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data = {"titre": "nouveau", "contenu": "dsfsdcvs"}
        url = news.get_api_url()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': 'test',
            'password': 'random'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            data = {"titre": "nouveau", "contenu": "dsfsdcvs"}
            news = News.objects.first()
            print(news.contenu)
            url = news.get_api_url()
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

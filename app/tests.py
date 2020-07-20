from datetime import datetime
import pytz
from time import process_time

from django.test import Client, TestCase, RequestFactory

from app.models import Url


class ShortenerTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.factory = RequestFactory()

    def test_index_view(self):
        response = self.client.get(f'/app/')

        self.assertEqual(response.status_code, 200)

    def test_shorten_view(self):
        response = self.client.post(f'/app/shorten/', {
            'url': 'www.google.com/django'
        })

        url_obj = Url.objects.get(long_url='www.google.com/django')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(url_obj.ip, '127.0.0.1')
        self.assertIsNotNone(url_obj.time)
        self.assertIsNotNone(url_obj.shortened_url)

    def test_redirecting_speed(self):
        for i in range(1000):
            url_obj = Url()
            url_obj.long_url = f'www.google.com/{i}'
            url_obj.time = datetime.now(pytz.utc)
            url_obj.shortened_url = url_obj.generate_id(6)
            url_obj.save()

        url_obj_500 = Url.objects.filter(long_url='www.google.com/500').first()

        start = process_time()
        for i in range(1000):
            response = self.client.get(f'/app/{url_obj_500.shortened_url}/')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, 'https://www.google.com/500')

        end = process_time()

        print(f'Process time with Redis: {end - start}')

    def test_redirecting_speed_without_redis(self):
        for i in range(1000):
            url_obj = Url()
            url_obj.long_url = f'www.google.com/{i}'
            url_obj.time = datetime.now(pytz.utc)
            url_obj.shortened_url = url_obj.generate_id(6)
            url_obj.save()

        url_obj_500 = Url.objects.filter(long_url='www.google.com/500').first()

        start = process_time()
        for i in range(1000):
            response = self.client.get(f'/app/detail_without_redis/{url_obj_500.shortened_url}/')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, 'https://www.google.com/500')

        end = process_time()

        print(f'Process time without Redis: {end - start}')

    def test_redirect_with_nonexisting_url(self):
        response = self.client.get(f'/app/invalid_url/')

        self.assertEqual(response.status_code, 404)

    def test_set_info(self):
        url = 'www.google.com'
        request = self.factory.get('/app/')

        url_obj = Url()
        url_obj.set_info(request, url)
        url_obj.save()

        self.assertEqual(url_obj.long_url, url)
        self.assertEqual(url_obj.ip, '127.0.0.1')
        self.assertIsNotNone(url_obj.time)
        self.assertIsNotNone(url_obj.shortened_url)

    def test_get_shorted_url(self):
        url_obj = Url()
        url_obj.shortened_url = 'AF45Dd'
        shortened_url = url_obj.get_shorted_url()

        self.assertEqual(shortened_url, f'localhost:8000/app/AF45Dd')

    def test_generate_id(self):
        size = 6
        id = Url.generate_id(size)

        self.assertEqual(len(id), size)

    def test_get_client_ip(self):
        request = self.factory.get('/app/')
        ip = Url.get_client_ip(request)

        self.assertEqual(ip, '127.0.0.1')

        request = self.factory.get('/app/', HTTP_X_FORWARDED_FOR="8.8.8.8")
        ip = Url.get_client_ip(request)
        self.assertEqual(ip, '8.8.8.8')

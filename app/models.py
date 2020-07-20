from datetime import datetime
import pytz
import random
import string

from django.db import models


class Url(models.Model):
    """
    Url is used to store shortened url version and record the click statistics for each short URLs.
    """

    shortened_url = models.CharField(max_length=50)
    long_url = models.CharField(max_length=2000)

    ip = models.CharField(max_length=45)
    time = models.DateTimeField()

    expiration_time = models.IntegerField(default=360)
    hit_counter = models.IntegerField(default=0)

    def set_info(self, request, url):
        self.long_url = url
        self.ip = self.get_client_ip(request)
        self.time = datetime.now(pytz.UTC)
        self.shortened_url = self.generate_id(6)

    def get_shorted_url(self):
        shortened_url = f'localhost:8000/app/{self.shortened_url}'
        return shortened_url

    @staticmethod
    def generate_id(size):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

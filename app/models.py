from datetime import datetime
import pytz
import random
import string

from django.conf import settings
from django.db import models

from app.helpers import get_client_ip


class UrlManager(models.Manager):
    def create_url(self, request, url):
        url_obj = self.create(
            long_url=url,
            ip=get_client_ip(request),
            time=datetime.now(pytz.UTC)
        )

        url_obj.set_short_url()

        return url_obj


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

    objects = UrlManager()

    @property
    def shorted_url(self):
        shortened_url = f'localhost:8000/app/shorten/{self.shortened_url}'
        return shortened_url

    def set_short_url(self):
        charset = string.ascii_uppercase + string.digits
        self.shortened_url = ''.join(random.choice(charset) for _ in range(settings.SHORT_URL_LEN))

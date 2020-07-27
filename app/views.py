from datetime import timedelta, datetime
import pytz

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView
import redis

from app.models import Url


class IndexView(TemplateView):
    template_name = "app/index.html"


class UrlView(View):
    def post(self, request):
        url = request.POST['url']
        url_obj = Url.objects.create_url(request, url)
        url_obj.save()

        short_url = url_obj.shorted_url
        template = loader.get_template('app/layout_SHORTURL.html')
        context = {
            'short_url': short_url,
            'url': url
        }
        return HttpResponse(template.render(context, request))

    def get(self, request, pk):
        redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     decode_responses=True)
        if pk in redis_instance:
            url_obj = redis_instance.lrange(pk, 0, 2)
            url_obj[0] = str(int(url_obj[0]) + 1)
            redis_instance.lpush(pk, url_obj[2],url_obj[1],url_obj[0])

            url = url_obj[2]
            expiration = url_obj[1]
            hit_counter = url_obj[0]
        else:
            url_obj = Url.objects.filter(shortened_url=pk).first()
            if not url_obj:
                return HttpResponseNotFound()

            expiration = str(url_obj.time + timedelta(seconds=url_obj.expiration_time))
            url = url_obj.long_url
            hit_counter = url_obj.hit_counter

            url_obj.hit_counter += 1
            url_obj.save()

            # LPUSH mylist a b c will result into a list containing c as first element, b as second
            # element and a as third element
            redis_instance.lpush(pk, url,expiration,str(hit_counter))

        if expiration >= str(datetime.now(pytz.UTC)) and int(hit_counter) < 1200:
            return HttpResponseRedirect(f'https://{url}')

        return HttpResponseNotFound()


class UrlWithoutRedisView(View):
    def get(self, request, pk):
        url_obj = Url.objects.filter(shortened_url=pk).first()
        if not url_obj:
            return HttpResponseNotFound()

        expiration = str(url_obj.time + timedelta(seconds=url_obj.expiration_time))
        url_obj.hit_counter += 1
        url_obj.save()

        if expiration >= str(datetime.now(pytz.UTC)) and int(url_obj.hit_counter) < 1200:
            return HttpResponseRedirect(f'https://{url_obj.long_url}')

        return HttpResponseNotFound()

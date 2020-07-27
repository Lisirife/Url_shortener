from django.urls import path

from app.views import IndexView, UrlView, UrlWithoutRedisView

urlpatterns = [
    path('index/', IndexView.as_view()),
    path('shorten/', UrlView.as_view()),
    path('shorten/<pk>/', UrlView.as_view(), name='detail'),
    path('detail_without_redis/<pk>', UrlWithoutRedisView.as_view(), name='detail_without_redis'),
]
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shorten/', views.shorten, name='shorten'),
    path('<id>/', views.detail, name='detail'),
    path('detail_without_redis/<id>/', views.detail_without_redis, name='detail_without_redis'),
]
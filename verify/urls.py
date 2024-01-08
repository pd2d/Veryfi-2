from django.urls import path, include
from .views import my_view,data,datas

urlpatterns = [
    path('list/', my_view, name='list'),
    path('view/', data, name='view'),
    path('views/', datas, name='views'),
]
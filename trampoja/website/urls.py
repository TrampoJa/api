from django.conf.urls import url
from django.contrib import admin
from website.views import *
from django.urls import path

from . import views

urlpatterns = [
    
    url(r'^$', views.Index.get, name='index'),
]
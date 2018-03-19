from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from mitosite import urls
from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^single/', views.SingleJob, name='single'),
    url(r'^paired/', views.PairedJob, name='paired'),
    url(r'^$', views.choose, name='choose'),
    url(r'^uploadtest/', views.index, name='uploadtest'),
    url(r'^loading/', views.loading, name='loading'),
    url(r'^tutorial/', views.tutorial, name='tutorial'),
    url(r'^programmes/', views.programmes, name='programmes'),
    url(r'^about/', views.about, name='about'),
    url(r'^retrieve/', views.RetrieveJob, name='retrieve'),
    url(r'^testresult/', views.testresult, name='testresult'),
    url(r'^styletest/', views.styletest, name='styletest'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
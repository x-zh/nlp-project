# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'qa.views',
    url(r'$', 'ask_me_anything'),
)

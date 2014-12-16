# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import os
import sys
_ = __file__
for i in range(4):
    _ = os.path.dirname(_)
sys.path.append(os.path.join(_, 'nlp_question_answer'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'nlp_question_answer.settings'

from scrapy.contrib.djangoitem import DjangoItem
from qa.models import Pages


class PagesItem(DjangoItem):
    django_model = Pages


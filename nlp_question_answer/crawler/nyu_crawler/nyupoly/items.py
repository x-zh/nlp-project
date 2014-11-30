# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Page(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()

    def __str__(self):
        return 'Title: %s\nLink: %s\nContent Size: %s' % (str(self['title']), str(self['link']), str(self['content'])[:50])

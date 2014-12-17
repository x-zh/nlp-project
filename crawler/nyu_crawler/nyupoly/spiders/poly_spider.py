# coding=UTF-8
import os
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from nyupoly.items import PagesItem, ParagraphItem
import codecs

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class LinksListSpider(Spider):
    name = 'nyupoly'
    allowed_domains = ['nyu.edu']
    base_url = 'http://engineering.nyu.edu'
    start_urls = []

    def start_requests(self):
        with open(os.path.join(BASE_DIR, 'linkslist.txt'), 'r') as ll:
            for l in ll:
                yield Request(l.strip(), self.parse)

    def joinwithoutempty(self, ll):
        res = []
        for l in ll:
            if l.strip():
                res.append(l.strip())
        return ' '.join(res)

    def parse(self, response):
        sel = Selector(response=response)
        p = PagesItem()
        p['url'] = response.url
        p['title'] = self.joinwithoutempty(sel.xpath('//title//text()').extract())
        p['h1'] = self.joinwithoutempty(sel.xpath('//h1//text()').extract())
        p['h2'] = self.joinwithoutempty(sel.xpath('//h2//text()').extract())
        p['h3'] = self.joinwithoutempty(sel.xpath('//h3//text()').extract())
        p['h4'] = self.joinwithoutempty(sel.xpath('//h4//text()').extract())
        p['h5'] = self.joinwithoutempty(sel.xpath('//h5//text()').extract())
        p['p'] = self.joinwithoutempty(sel.xpath('//p//text()').extract())
        for pt in sel.xpath('//div//text()').extract():
            if pt.strip() and len(pt.strip()) > 2:
                pp = ParagraphItem()
                pp['url'] = response.url
                pp['content'] = pt
                pp['title'] = p['title']
                pp.save()
        p['div'] = self.joinwithoutempty(sel.xpath('//body//text()').extract())
        p.save()
        with codecs.open('shabi.txt', 'a', 'utf-8') as f:
            f.write(p['title'])
            f.write(p['p'])
        yield p

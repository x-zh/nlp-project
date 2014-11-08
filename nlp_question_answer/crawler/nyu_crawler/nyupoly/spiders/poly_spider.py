# coding=UTF-8

"""
Created on 11/6/14

@author: 'johnqiao'

Usage:

scrapy crawl nyupoly -o nyupoly.json -t json

"""
import json
import os
import re
import sys
import threading
import urlparse

from BeautifulSoup import BeautifulSoup

from scrapy import Spider, Selector, Request


reload(sys)
sys.setdefaultencoding('utf-8')


def threadsafe_function(fn):
    """decorator making sure that the decorated function is thread safe"""
    lock = threading.Lock()

    def new(*args, **kwargs):
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()
        return r

    return new


class PolyMajorsAndProgramsSpider(Spider):
    name = 'nyupoly'
    allowed_domains = ['engineering.nyu.edu']
    base_url = 'http://engineering.nyu.edu'
    start_urls = [
        # base_url,
        os.path.join(base_url, 'academics/programs'),
    ]
    data_filename = 'nyupoly-data.json'
    # links we already crawled
    links_crawled_pool = set()
    max_pages = 3000
    page_processed = 0
    page_enqueued = 0
    error_count = 0

    is_in_memory_crawl = True
    in_memory_pages = []
    in_memory_pages_size = 10
    in_memory_pages_count = 0

    def parse(self, response):
        self.print_crawler_info(response)
        # create data file if it doesn't exist
        self.create_json_data_file()
        hxs = Selector(response)
        links = hxs.xpath('//a/@href').extract()
        # Pattern to check proper link
        link_pattern = re.compile(
            '^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$')
        for link in links:
            link = str(link)
            if link.startswith('/') and 'mailto:' not in link:
                link = urlparse.urljoin(self.base_url, link)
            else:
                # Drop the links start with 'http://', since they are probably an external link.
                continue
            # If it is a proper link and is not checked yet, yield it to the Spider.
            if link_pattern.match(link) and not link in self.links_crawled_pool:
                if self.page_enqueued > self.max_pages:
                    break
                self.page_enqueued += 1
                self.links_crawled_pool.add(link)
                # yield Request(url=link, callback=self.parse_page, errback=self.error_handler)
                yield Request(link, callback=self.parse, errback=self.error_handler)
        yield self.parse_page(response)

    @threadsafe_function
    def parse_page(self, response):
        self.page_processed += 1
        sel = Selector(response)
        title = ' '.join([c.extract() for c in sel.css('html head title::text')])
        content = '\n'.join([self.pure_text(c.extract()) for c in sel.css('#container .content p')])
        if len(content):
            # Output as json file
            page = {
                'title': title,
                'link': response.url,
                'content': content.strip()
            }

            if self.is_in_memory_crawl:
                self.in_memory_pages.append(page)
                self.in_memory_pages_count += 1
                if self.in_memory_pages_count >= self.in_memory_pages_size:
                    self.in_memory_pages_count = 0
                    self.output_into_json()
                    self.in_memory_pages = []
            else:
                with open(self.data_path(), mode='r') as f:
                    data = json.load(f)
                with open(self.data_path(), mode='w') as f:
                    data.append(page)
                    json.dump(data, f)

            # from ..items import Page
            # page = Page()
            # page['title'] = title
            # page['link'] = response.url
            # page['content'] = content
            # return page

    def error_handler(self, e):
        self.error_count += 1

    def pure_text(self, text):
        soup = BeautifulSoup(text)
        s = str(''.join(soup.findAll(text=True))).strip()
        s = ' '.join(line.strip() for line in s.split("\n"))
        return s

    def create_json_data_file(self):
        if not os.path.isfile(self.data_path()):
            with open(self.data_path(), mode='w') as f:
                json.dump([], f)

    def data_path(self):
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        data_path = os.path.join(os.path.join(data_dir, 'data'), self.data_filename)
        return data_path

    def print_crawler_info(self, response):
        print 'pool size: %d/%d page enqueued: %d page processed: %d link: ...%s' % (
            len(self.links_crawled_pool), self.max_pages, self.page_enqueued, self.page_processed, response.url[-10:])

    def output_into_json(self):
        if self.is_in_memory_crawl:
            with open(self.data_path(), mode='r') as f:
                data = json.load(f)
            with open(self.data_path(), mode='w') as f:
                data.extend(self.in_memory_pages)
                json.dump(data, f)

    def closed(self, reason):
        self.output_into_json()

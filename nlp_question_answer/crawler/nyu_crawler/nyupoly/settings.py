# -*- coding: utf-8 -*-

# Scrapy settings for nyupoly project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nyupoly'

SPIDER_MODULES = ['nyupoly.spiders']
NEWSPIDER_MODULE = 'nyupoly.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nyupoly (+http://www.yourdomain.com)'

LOG_LEVEL = 'INFO'
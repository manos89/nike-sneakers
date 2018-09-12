# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class SnkrsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shoe = scrapy.Field(output_processor=TakeFirst())


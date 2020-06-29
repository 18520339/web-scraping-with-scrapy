# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    titles = scrapy.Field()
    votes = scrapy.Field()
    reviews = scrapy.Field()
    prices = scrapy.Field()
    image_links = scrapy.Field()
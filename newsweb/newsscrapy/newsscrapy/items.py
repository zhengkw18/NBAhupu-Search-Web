# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from newsapp import  models
class NewsscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ScrapyPlayer(scrapy.Item):
    id=scrapy.Field()
    name=scrapy.Field()
    team=scrapy.Field()
class ScrapyArticle(scrapy.Item):
    id=scrapy.Field()
    title=scrapy.Field()
    source=scrapy.Field()
    datetime=scrapy.Field()
    content=scrapy.Field()
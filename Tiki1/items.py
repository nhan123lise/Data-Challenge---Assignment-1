# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Tiki1Item(scrapy.Item):

    NAME = scrapy.Field()
    AUTHOR = scrapy.Field()
    REVIEWS = scrapy.Field()
    PRICE_SALE = scrapy.Field()
    PRICE_REGULAR = scrapy.Field()
    DISCOUNT = scrapy.Field()
    TIKINOW = scrapy.Field()
    RATES = scrapy.Field()

    pass

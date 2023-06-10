# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Director = scrapy.Field()
    Rating = scrapy.Field()
    Genre = scrapy.Field()
    Certificate = scrapy.Field()
    Year = scrapy.Field()

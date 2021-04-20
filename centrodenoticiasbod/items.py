import scrapy


class CcentrodenoticiasbodItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()

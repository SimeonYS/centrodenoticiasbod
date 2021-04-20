import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CcentrodenoticiasbodItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class PrensaSpider(scrapy.Spider):
    name = 'prensa'
    start_urls = ['http://centrodenoticiasbod.com.ve/category/pase-de-prensa-b-o-d/']
    ITEM_PIPELINES = {
        'prensa.pipelines.CcentrodenoticiasbodPipeline': 300,
    }

    def parse(self, response):
        post_links = response.xpath('//a[@class="more-link btn alt"]/@href').getall()
        yield from response.follow_all(post_links, self.parse_post)

        next_page = response.xpath('//div[@class="col-md-6 nav-post-prev"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        date = response.xpath('//div[@class="post-date"]/text()').get()
        category = response.xpath('//div[@class="post-categories"]/a[@rel="category tag"]/text()').get()
        title = response.xpath('//h1/text()').get()
        content = response.xpath('//div[@class="entry-content"]//text()').getall()
        content = [p.strip() for p in content if p.strip()]
        content = re.sub(pattern, "", ' '.join(content))

        item = ItemLoader(item=CcentrodenoticiasbodItem(), response=response)
        item.default_output_processor = TakeFirst()

        item.add_value('title', title)
        item.add_value('category', category)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('date', date)

        yield item.load_item()
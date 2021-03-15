import scrapy

from scrapy.loader import ItemLoader

from ..items import CofidishuItem
from itemloaders.processors import TakeFirst


class CofidishuSpider(scrapy.Spider):
	name = 'cofidishu'
	start_urls = ['https://www.cofidis.hu/blog/index']

	def parse(self, response):
		post_links = response.xpath('//a[@class="post-more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article[@class="blog-content-wrap blog-post"]/p//text()[normalize-space()]|//article[@class="blog-content-wrap blog-post"]/h2//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="post-meta"]/text()').get()

		item = ItemLoader(item=CofidishuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

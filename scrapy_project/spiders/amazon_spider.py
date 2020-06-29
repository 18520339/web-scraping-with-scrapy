import os
import re
import requests
import scrapy
from ..items import ScrapyProjectItem

class AmazonSpider(scrapy.Spider):

	name = 'amazon'
	start_urls = [
		'https://www.amazon.com/Best-Sellers/zgbs/amazon-devices/'
	]
	image_index = 0

	def parse(self, response):
		items = ScrapyProjectItem()
		all_products = response.css('li.zg-item-immersion')

		for product in all_products:
			titles = product.css('div.p13n-sc-truncate::text').extract()
			titles = [title.replace('\n', '').strip() for title in titles]

			votes = product.css('.a-icon-alt::text').extract()
			votes = [vote[:3] for vote in votes]

			reviews = product.css('.a-size-small::text').extract()
			reviews = [review.replace(',', '') for review in reviews]

			prices = product.css('.p13n-sc-price::text').extract()
			prices = [price[1:] for price in prices]

			image_links = product.css('.a-spacing-small img::attr(src)').extract()
			AmazonSpider.download_image(image_links, 'images crawled')

			items['titles'] = titles
			items['votes'] = votes
			items['reviews'] = reviews
			items['prices'] = prices
			items['image_links'] = image_links

			yield items

		# Đi tới trang tiếp theo
		next_page = response.css('li.a-last a::attr(href)').get()

		if next_page is not None:
			# Gọi đệ quy tới khi trang rỗng
			yield response.follow(next_page, callback = self.parse) 


	@staticmethod
	def download_image(image_urls, images_folder_name):
		if not os.path.exists(images_folder_name):
			os.makedirs(images_folder_name)

		for url in image_urls:
			image_format = re.search(r'/([\w_.,%-]+[.](jpg|gif|png))$', url)
			AmazonSpider.image_index += 1

			if image_format:
				filename = images_folder_name + '/item ' + \
					str(AmazonSpider.image_index) + '.' + image_format.group(2)
								
				with open(filename, 'wb') as file:
					if 'http' not in url:
						url = '{}{}'.format(AmazonSpider.start_urls[0], url)
					response = requests.get(url)
					file.write(response.content)
			
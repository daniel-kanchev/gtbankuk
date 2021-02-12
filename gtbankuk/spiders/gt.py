import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from gtbankuk.items import Article


class GtSpider(scrapy.Spider):
    name = 'gt'
    start_urls = ['https://www.gtbankuk.com/media-centre']

    def parse(self, response):
        links = response.xpath('//div[@class="article-list-item-title"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="banner-parent-title"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="post-date"]/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d %b %y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="col-sm-8 col-custom-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()

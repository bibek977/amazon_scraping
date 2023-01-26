import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AmazonScrapingItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/ASUS-IPS-Type-i5-10300H-Processor-FX506LH-AS51/dp/B09SVQ25XH/ref=sr_1_2?keywords=gaming+laptop&qid=1674716642&sprefix=gaming+lapa%2Caps%2C382&sr=8-2'
    ]

    def parse(self, response):
        review = response.xpath('//div[@data-hook="global-customer-reviews-widget"]//a[@data-hook="see-all-reviews-link-foot"]/@href').extract_first()

        yield response.follow('https://www.amazon.com' + review, callback = self.parse_page)

    def parse_page(self,response):
        items = AmazonScrapingItem()
        name = response.xpath('//div[@data-hook="review"]//span[@class="a-profile-name"]/text()').extract()
        title = response.xpath('//a[@data-hook="review-title"]/span/text()').extract()
        date = response.xpath('//span[@data-hook="review-date"]/text()').extract()
        body = response.xpath('//span[@data-hook="review-body"]/span/text()').extract()


        items['name'] = name
        items['title'] = title
        items['date'] = date
        items['body'] = body

        yield items

        next_page = response.css('.a-last > a::attr(href)').extract_first()

        if next_page is not None:
            yield response.follow('https://www.amazon.com' + next_page, callback = self.parse_page)
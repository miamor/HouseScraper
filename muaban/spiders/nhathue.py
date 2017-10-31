# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from muaban.items import muabanItem


class HouseSpider(CrawlSpider):
    name = "nhathue"
    allowed_domains = ["muaban.net"]
    start_urls = []
    for i in range(1,2):
        start_urls.append('https://muaban.net/nha-tro-phong-tro-ha-noi-l24-c3405?cp=%d' % i)

    rules = (
        Rule(LinkExtractor(allow=(), ),
             callback="parse_item",
             follow=False),)

    def parse_item(self, response):
        item_links = response.css('.mbn-image::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        title = response.css('h1::text').extract()[0].strip()
        price = response.css('.price-value::text').extract()[0].strip()
        phone = response.css('.contact-mobile > span::text').extract()[0].strip()
        des = response.css('.ct-body::text').extract()[0]
        contact_name = response.css('.contact-name::text').extract()[0].strip()
        adr_details = response.css('.ct-contact > .clearfix:nth-child(1) > .contact-name::text').extract()[0].strip()
        adr = response.css('.cl-price-sm > .visible-lg:nth-child(2)::text').extract()[0].strip()

        item = muabanItem()
        item['title'] = title
        item['price'] = price
        item['phone'] = phone
        item['address'] = (adr_details if adr_details != contact_name else adr)
        item['contact_name'] = contact_name
        item['des'] = des
        item['available'] = 0
        item['type'] = 'S'
        item['url'] = response.url

        yield item

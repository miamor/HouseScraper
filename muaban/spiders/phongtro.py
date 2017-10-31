# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from muaban.items import muabanItem

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class HouseSpider(CrawlSpider):
    name = "phongtro"
    allowed_domains = ["phongtro123.com"]
    start_urls = []
    for i in range(1,3):
        start_urls.append('https://phongtro123.com/tim-kiem/page/%d?type=3&tinh=41&quan=0&duong=0&price=0&dientich=0'%i)
    """
    for i in range(1,2):
        # type=1 (phòng trọ) (S)
        # type=2 (nhà thuê nguyên căn) (L1)
        # type=3 (thuê căn hộ chung cư) (L2)
        for j in range(1,3):
            start_urls.append('https://phongtro123.com/tim-kiem/page/%d?type=%d&tinh=41&quan=0&duong=0&price=0&dientich=0'%i%j)
    """

    rules = (
        Rule(LinkExtractor(allow=('^https://phongtro123.com/tinh-thanh/ha-noi/.*'), ),
             callback="parse_item",
             follow=False),)

    def parse_item(self, response):
        item_links = response.css('.post_info > .post-link::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        sel = Selector(response)
        images = sel.xpath('//img[@class="photo_item_image"]')
        imgAr = []
        for img in images:
            iurl = img.xpath('./@src').extract() or ''
            item_iurl = iurl[0] if iurl else ''
            imgAr.append(item_iurl)
        print(imgAr)

        title = response.css('.post-title-lg > .post-link::text').extract()[0].strip()
        price = response.css('.summary_item_info_price::text').extract()[0].strip()
        des = response.css('#motachitiet > p::text').extract()[0]
        adr_details = response.css('.post_summary > .summary_row:nth-child(1) .summary_item_info::text').extract()[0].strip()
        area = response.css('.summary_item_info_area::text').extract()[0].strip()
        contact_name = response.css('.post_summary > .summary_row:nth-child(3) > .post_summary_left > .summary_item_info::text').extract()[0].strip()
        contact_email = response.css('.post_summary > .summary_row:nth-child(4) > .post_summary_left > .summary_item_info::text').extract()[0].strip()
        phone = response.css('.summary_item_info_phone > a::text').extract()[0].strip()

        date = sel.xpath('//meta[@property="article:modified_time"]').xpath('./@content').extract()

        outdated = sel.xpath('//div[id="da_het_han"]')
        if outdated :
            print 'outdated'
        else :
            item = muabanItem()
            item['title'] = title
            item['price'] = price
            item['phone'] = phone
            item['address'] = adr_details
            item['contact_name'] = contact_name
            item['des'] = des
            item['available'] = 0
            item['url'] = response.url
            item['type'] = 'L2'
            item['contact_email'] = contact_email
            item['area'] = area
            item['thumbs'] = imgAr
            item['date'] = date

        yield item

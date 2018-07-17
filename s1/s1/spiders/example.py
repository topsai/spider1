# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import time


class ExampleSpider(scrapy.Spider):
    name = 'example'  # 工程唯一标识
    # allowed_domains = ['example.com']
    BaseUrl = 'http://www.dytt8.net'
    start_urls = [BaseUrl]

    def parse(self, response):
        # print(response.url)
        # print(response.text)
        # print(response.body)
        # print(response.css())
        # print(response.xpath().extract())
        # 版块
        # //div[@class ='co_area2']/div[1]/p/em/a/@href
        homemodule = response.xpath('//div[@class="title_all"]/p')
        for i in homemodule:
            # print(i)
            title = i.xpath('strong/text()').extract()
            if title:
                href = i.xpath('em/a/@href').extract()
                if href:
                    title = title[0]
                    href = href[0]
                    if self.BaseUrl not in href:
                        href = self.BaseUrl + href
                    print(title, href)
                    yield Request(href, callback=self.movie)
        # todo 翻页没做完
        nexturl = response.xpath('//link[@rel="next"]/@href').extract()
        if nexturl:
            nexturl = nexturl[0]
            req_url = baseurl + nexturl
            yield Request(req_url, callback=self.parse)

        # response.xpath('//div[@class="co_area2"]/div[1]/p/strong/text()').extract()
        # print(homepage)
        #
        # a = response.xpath('//div[@class="co_area2"]')
        # for i in a:
        #     print(i.xpath('//div'))
        # print(i.xpath('//div[1]/ul/table/'))
        # 电影名称
        # print(response.xpath('//div[@class="co_area2"]/div[2]//td[1]/a[2]/text()').extract())
        # // *[ @ id = "header"] / div / div[3] / div[2] / div[2] / div[1] / div / div[2] / div[2] / ul / table / tbody / \
        # tr[2] / td[1] / a[2]
        # print(response.xpath('//div[@class="title_all"]/p/text()').extract())

    def login(self):
        pass

    def movie(self, response):
        # page = response.xpath('//div[class="co_content8"]')
        time.sleep(1)
        print('----------movie--------------')
        page = response.xpath('//table')
        for i in page:
            temp = i.xpath('tr[2]/td[2]/b/a[2]')
            href = temp.xpath('@href')
            name = temp.xpath('text()')
            if href and name:
                href = href.extract()[0]
                name = name.extract()[0]
                print(href, name)

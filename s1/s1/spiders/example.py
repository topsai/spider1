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
        # 主页大板块
        # homemodule = response.xpath('//div[@class="title_all"]/p')
        # for i in homemodule:
        #     if not i:
        #         continue
        #     # print(i)
        #     title = i.xpath('strong/text()').extract()
        #     if title:
        #         href = i.xpath('em/a/@href').extract()
        #         if href:
        #             title = title[0]
        #             href = href[0]
        #             if self.BaseUrl not in href:
        #                 href = self.BaseUrl + href
        #             print(title, href)
        #             yield Request(href, callback=self.movie)
        # todo 翻页没做完

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
        href = "http://www.ygdy8.net/html/gndy/oumei/index.html"
        return Request(href, callback=self.movie)

    def login(self):
        pass

    def movie(self, response):
        # page = response.xpath('//div[class="co_content8"]')

        print('----------movie--------------')
        print(response.url)
        page = response.xpath('//table')
        for i in page:
            temp = i.xpath('tr[2]/td[2]/b/a[2]')
            href = temp.xpath('@href')
            name = temp.xpath('text()')
            if href and name:
                href = href.extract()[0]
                name = name.extract()[0]
                # print(href, name)
                print("找到电影：", name, href)
                yield Request(self.BaseUrl+href, callback=self.info)
        # 查询翻页
        nexturl = response.xpath('//a[contains(text(), "下一页")]')
        # 电影类型
        title = response.xpath('//title/text()').extract()[0].split('_')[0]

        try:
            if nexturl.xpath('text()').extract()[0] == "下一页":
                print('----翻页----')
                nexturl = nexturl.xpath('@href')
                if nexturl:
                    nexturl = nexturl.extract()[0]
                    nextpage = nexturl.strip(".html").rsplit("_", 1)[1]
                    req_url = response.url.rsplit("/", 1)[0] + "/" + nexturl
                    print("即将前往 ", title, " 第", nextpage, "页")
                    yield Request(req_url, callback=self.movie)
            else:
                print('到底了')
        except:
            print('翻页失败-err')
            print(response.url)

    def info(self, response):
        print("info")
        print(response.url)
        xunlei = response.xpath('//table[@align="center"]/tbody/tr/td/a/text()').extract()[0]
        image = response.xpath('//img/@src').extract()[1]
        print(image, xunlei)

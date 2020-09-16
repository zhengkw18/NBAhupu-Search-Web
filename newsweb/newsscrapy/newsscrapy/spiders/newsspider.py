# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import datetime
from newsscrapy.items import ScrapyArticle
from newsapp.models import Spider
class NewsspiderSpider(scrapy.Spider):
    name = 'newsspider'
    allowed_domains = ['voice.hupu.com']
    start_urls = ['http://voice.hupu.com/nba/']
    def parse(self, response):
        #while True:
            for i in range(1,6):
                sp = Spider.objects.all().get(id=1)
                if sp.status=='ON':
                    yield Request(url="http://voice.hupu.com/nba/" + str(i), callback=self.parse_f, dont_filter=True)
    def parse_f(self,response):
        urls = response.css(".list-hd h4 a::attr(href)").extract()
        for url in urls:
            yield Request(url=url, callback=self.parse_detail)
    def parse_detail(self,response):
        title = response.css("h1.headline::text").extract_first("Unknown Title").replace("\r","").replace("\n","").strip()
        source = response.css("span.comeFrom a::text").extract_first("Unknown source").replace("\r","").replace("\n","").strip()
        dt = datetime.datetime.strptime(response.css("a.time span::text").extract_first("1000-01-01 00:00:00").replace("\r","").replace("\n","").strip(),"%Y-%m-%d %H:%M:%S")
        cs = response.css(".artical-main-content p::text").extract()
        clist = [c.replace("\r","").replace("\n","").strip() for c in cs]
        content = "\n".join(clist)
        yield ScrapyArticle(id="1",title=title,source=source,datetime=dt,content=content)
        pass
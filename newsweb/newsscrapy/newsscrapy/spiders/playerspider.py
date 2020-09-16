# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import  Request
from newsscrapy.items import ScrapyPlayer
class PlayerspiderSpider(scrapy.Spider):
    name = 'playerspider'
    allowed_domains = ['nba.hupu.com']
    start_urls = ['https://nba.hupu.com/players/rockets']

    def parse(self, response):
        yield Request(url=response.url, callback=self.parse_detail)
        urls = response.css("ul.players_list li span.team_name a::attr(href)").extract()
        for url in urls:
            yield Request(url=url,callback=self.parse_detail)
        pass
    def parse_detail(self, response):
        titlesrc = response.css("title::text").extract_first("").strip().replace("\r","").replace("\n","")
        match_re = re.match(r"^([A-Za-z0-9\u4e00-\u9fa5]+)队球员名单",titlesrc)
        if match_re:
            title = match_re.group(1)

        names = response.css("table.players_table tbody tr td.left b a::text").extract()
        for name in names:
            player = ScrapyPlayer(name=name,team=title,id="0")
            yield player
        pass
# -*- coding: UTF-8 -*-
import scrapy
from functools import partial
import pymongo


class MoviesSpider(scrapy.Spider):
    # 爬歌单
    name = "play_list"

    def __init__(self, start, times):
        # start和times为倍数值
        # 例如start为0，times为5，即从0开始取5*35条数据
        # python -m scrapy crawl play_list -a start=0 -a times=1000
        self.start = int(start)
        self.times = int(times)
        client = pymongo.MongoClient(host='localhost', port=27017)
        self.collection = client['m163']['lists']

    def start_requests(self):
        for i in range(self.start, self.start + self.times):
            yield scrapy.Request(url='https://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=' +
                                     str(i * 35), method='GET', dont_filter=True,
                                 callback=partial(self.parse))

    def parse(self, response):
        play_lists = response.css('#m-pl-container li')
        for li in play_lists:
            data = {
                'title': li.css('.dec .tit::text').extract()[0],
                'id': li.css('.dec .tit::attr(href)').extract()[0].replace("/playlist?id=", "")
            }
            self.collection.insert_one(data)



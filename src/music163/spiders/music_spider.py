# -*- coding: UTF-8 -*-
import scrapy
from functools import partial
import pymongo


class MoviesSpider(scrapy.Spider):
    # 爬歌曲信息和id
    name = "music"

    def __init__(self):
        # python -m scrapy crawl music
        client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = client['m163']

    def start_requests(self):
        for music_list in self.db['lists'].find():
            yield scrapy.Request(url='https://music.163.com/playlist?id=' + music_list['id'], method='GET',
                                 dont_filter=True, callback=partial(self.parse))

    def parse(self, response):
        play_lists = response.css('.f-hide li')
        for li in play_lists:
            data = {
                'title': li.css('a::text').extract()[0],
                'id': li.css('a::attr(href)').extract()[0].replace("/song?id=", "")
            }
            self.db['musict'].insert_one(data)



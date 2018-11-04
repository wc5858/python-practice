# -*- coding: UTF-8 -*-
import scrapy
from functools import partial
import pymongo
import json


class MoviesSpider(scrapy.Spider):
    # 爬评论
    name = "hots"

    def __init__(self):
        client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = client['m163']

    def start_requests(self):
        for song in self.db['music_distinct'].find():
            if 'ok2' not in song:
                yield self.deal(song['id'], 0, song['title'])

    def deal(self, song_id, idx, title):
        return scrapy.Request(url='http://music.163.com/api/v1/resource/comments/R_SO_4_' + song_id
                                  , method='GET', dont_filter=True,
                              callback=partial(self.parse, id=song_id, next=idx+1, title=title))

    def parse(self, response, id, next, title):
        data = json.loads(response.body)
        for i in data['hotComments']:
            i['song_id'] = id
            i['title'] = title
            self.db['hots'].insert_one(i)
        self.db['music_distinct'].update({'id': id}, {'$set': {'ok2': 1}})




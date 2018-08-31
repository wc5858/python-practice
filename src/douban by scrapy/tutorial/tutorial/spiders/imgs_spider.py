# -*- coding: UTF-8 -*-
import scrapy
import json
import MySQLdb
from functools import partial
from ..items import DoubanImgsItem


class MoviesSpider(scrapy.Spider):
    name = "imgs"

    def __init__(self, start, num):
        # 从指定文件中读若干行数据
        # python -m scrapy crawl imgs -a start=0 -a num=100
        self.start = start
        self.num = num
        self.db = MySQLdb.connect(host="47.75.87.109", port=3306,
                                  user="root", db="spider", passwd="root", charset='utf8')

    def __del__(self):
        self.db.close()

    def start_requests(self):
        cursor = self.db.cursor()
        sql = "SELECT id FROM movies LIMIT %s, %s" % (self.start, self.num)
        # try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for i in results:
            yield self.deal(str(i[0]), 0)

    def deal(self, id, start):
        return scrapy.Request(
            url='https://movie.douban.com/subject/' + id + '/photos?type=S&start=' +
                str(start) + '&sortby=like&size=a&subtype=c',
            callback=partial(self.parse, id=id, next=start + 30))

    def parse(self, response, id, next):
        list_imgs = response.css(
            '#content .article .poster-col3 li a img::attr(src)').extract()
        if list_imgs:
            yield self.deal(id, next)
            item = DoubanImgsItem()
            item['image_urls'] = list_imgs
            item['id'] = id
            yield item
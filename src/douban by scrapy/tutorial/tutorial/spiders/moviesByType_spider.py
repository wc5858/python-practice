# -*- coding: UTF-8 -*-
import scrapy
import json
from functools import partial
import MySQLdb


class MoviesSpider(scrapy.Spider):
    name = "moviesByType"

    def __init__(self, start, times):
        # start和times为倍数值
        # 例如start为0，times为5，即从0开始取100条数据
        # python -m scrapy crawl moviesByType -a start=0 -a times=1000
        self.start = int(start)
        self.times = int(times)
        # 写入数据库
        self.db = MySQLdb.connect(host="***********", port=3306,
                                  user="root", db="spider", passwd="root", charset='utf8')

    def __del__(self):
        self.db.close()

    def start_requests(self):
        for i in range(self.start, self.start + self.times):
            for j in ['剧情', '喜剧', '动作', '爱情', '科幻', '悬疑', '惊悚', '恐怖', '犯罪', '同性',
                      '音乐', '歌舞', '传记', '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠', '情色']:
                yield scrapy.Request(
                    url='https://movie.douban.com/j/new_search_subjects?sort=S&range=0,100&tags=电影,' + j + '&start=' +
                        str(i * 20),
                    callback=partial(self.parse, type=j))

    def parse(self, response, type):
        data = json.loads(response.body)['data']
        cursor = self.db.cursor()
        for i in data:
            sql = "SELECT * FROM movies WHERE id = '%s'" % (
                i['id'].encode("utf-8"))
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) > 0:
                    t = results[0][-1].encode("utf-8")
                    if t.find(type) == -1:
                        self.update(i['id'].encode("utf-8"), t+','+type)
                else:
                    self.insert(i, type)
            except:
                self.insert(i, type)

    def insert(self, i, type):
        cursor = self.db.cursor()
        sql = "INSERT INTO movies(title, id, cover, rate, url,type) \
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s' )" % \
            (i['title'].encode("utf-8"), i['id'].encode("utf-8"), i['cover'].encode(
                "utf-8"), i['rate'].encode("utf-8"), i['url'].encode("utf-8"), type)
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            print('sql err')
            self.db.rollback()

    def update(self, id, type):
        cursor = self.db.cursor()
        sql = "UPDATE movies SET type = '%s' WHERE id = '%s'" % (type, id)
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

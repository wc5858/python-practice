# -*- coding: UTF-8 -*-    
import scrapy
import json

class MoviesSpider(scrapy.Spider):
    name = "movies"

    def __init__(self, start, times):
        # start和times为倍数值
        # 例如start为0，times为5，即从0开始取100条数据
        # scrapy crawl movies -a start=0 -a times=2 -o movies/data4.csv
        self.start = int(start)
        self.times = int(times)

    def start_requests(self):
        for i in range(self.start, self.start + self.times):
            yield scrapy.Request(
                url='https://movie.douban.com/j/new_search_subjects?sort=S&range=0,100&tags=电影&start=' + str(i * 20),
                callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        # data = yaml.load(response.body)['data']
        data = json.loads(response.body)['data']
        for i in data:
            yield {
                'title': i['title'],
                'id': i['id'],
                'cover': i['cover'],
                'rate': i['rate'],
                'url': i['url'],
            }


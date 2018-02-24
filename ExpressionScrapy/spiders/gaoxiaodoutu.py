# -*- coding: utf-8 -*-
import json

import scrapy
import time

# 搞笑斗图大师
from ExpressionScrapy.items import GaoxiaodoutuCategoryItem, GaoxiaodoutuItem


class GaoxiaodoutuSpider(scrapy.Spider):
    name = "gaoxiaodoutu"
    allowed_domains = ["erp.xianwan.com"]
    start_urls = ['http://erp.xianwan.com/api/v4/Category/getRandList',
                  'http://erp.xianwan.com/api/v4/AmuseImages/getList']
    headers = {
        "Accept": "*/*",
        'Accept-Encoding': 'gzip',
        "Accept-Language": "*/*",
        'User-Agent': 'okhttp/3.4.1',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
    }
    category_form = {"sign": "78296ab09234aef8ecf4177f836c89ef", "key": "h32nfow45e", "deviceid": "865372028556774",
                     "os": "1", "version": "3.4.1", "timestamp": str((int)(time.time()))}

    # 获取种类
    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url, callback=self.parse_category, method="POST", headers=self.headers,
                             body=json.dumps(self.category_form))

    def parse_category(self, response):
        print("开始解析Category页面")
        # print(response.text)
        result = json.loads(response.text)
        list = result["result"]
        if list:
            for category in list:
                item = GaoxiaodoutuCategoryItem()
                item['category_name'] = category['category_name']
                item['category_id'] = category['id']
                # print(item['category_id'])
                yield item
                self.category_form['page'] = '0'
                self.category_form['category_id'] = category['id']
                yield scrapy.Request(url=self.start_urls[1], callback=self.parse_item, method='POST',
                                     headers=self.headers, body=json.dumps(self.category_form))
        print("结束解析Category页面")

    def parse_item(self, response):
        print("开始解析Item页面")
        result = json.loads(response.text)
        list = result['result']
        if list:
            for pic in list:
                item = GaoxiaodoutuItem()
                item['category_id'] = pic['category_id']
                item['dateline'] = pic['dateline']
                item['pic_id'] = pic['id']
                item['url'] = pic['url']
                yield item
        print("结束解析Item页面")

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



# 搞笑斗图种类Item
class GaoxiaodoutuCategoryItem(scrapy.Item):
    category_name = scrapy.Field()
    category_id = scrapy.Field()
    pass

# 搞笑斗图Item
class GaoxiaodoutuItem(scrapy.Item):
    category_id = scrapy.Field()
    url = scrapy.Field()
    dateline = scrapy.Field()
    pic_id = scrapy.Field()
    pass





# 从mongodb从取数据
import time
from pymongo import MongoClient
from urllib import request
import os
from PIL import Image
from multiprocessing import Pool

#  本地保存图片，以及上传图片
class PicUtil(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client['gaoxiaodoutu']
        category_table = db['GaoxiaodoutuCategoryItem']
        item_table = db['GaoxiaodoutuItem']
        # 保存文件夹名
        self.base_pic_folder = os.path.join("E:\Expression", 'Pic')
        if not os.path.exists(self.base_pic_folder):
            os.mkdir(self.base_pic_folder)
        # 种类表
        self.category_table = category_table
        # 图片表
        self.item_table = item_table

    # 表情包数量
    def get_pic_count(self):
        return self.item_table.count()

    # 下载图片
    def download_pic(self):
        for item_category in self.category_table.find():
            category_id = item_category['category_id']
            category_name = item_category['category_name']
            folder = os.path.join(self.base_pic_folder, category_name)
            if os.path.exists(folder):
                continue
            os.mkdir(folder)
            for item_pic in self.item_table.find():
                if item_pic['category_id'] == category_id:
                    url = item_pic['url']
                    pic_name = url.split("/")[-1]
                    # 下载图片
                    request.urlretrieve(url, os.path.join(folder, pic_name))
                    # 暂停一秒
                    time.sleep(1)
                    print("成功下载图片" + pic_name)

    # 下载状态监听
    def download_status(self):
        pass

    # 删除空文件夹
    def delete_empty_folder(self):
        files = os.listdir(self.base_pic_folder)
        for file in files:
            if os.path.isdir(file):
                if not os.listdir(file):
                    os.rmdir(file)


if __name__ == '__main__':
    pic_util = PicUtil()
    #多线程爬取
    pool=Pool()
    pic_util.download_pic()
    print("下载结束")
    pic_util.delete_empty_folder()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from NanRenTuan import settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from  dboperator import DBOperator
import MySQLdb
import MySQLdb.cursors
import logging
from scrapy.utils.log import configure_logging




class NanrentuanPipeline(ImagesPipeline):
    dbpool = DBOperator()

    def get_media_requests(self, item, info):  # 重写ImagesPipeline   get_media_requests方法
        sql = ("INSERT INTO tbl_movie (actress_name,movie_id, movie_name, movie_date)"
               "VALUES (%s, %s, %s, %s)")
        self.dbpool.insert(sql,(item['actress_name'],item['Fanhao'],item['name'],item['date']))
        logging.info("Item:Fanhao:%s,Actress:%s,name:%s,date:%s" %(item['Fanhao'],item['actress_name'],item['name'],item['date']))
        for image_url in item['image_urls']:
            meta = {'filename': u'%s/%s.jpg' % (item['actress_name'], item['Fanhao'])}  # 将文件名通过item传入到meta里面，然后再file_path里面调用
            yield scrapy.Request(url=image_url, meta=meta)

    def file_path(self, request, response=None, info=None):
        image_guid = request.meta.get('filename', '')
        return 'full/%s' % (image_guid)

    def item_completed(self, results, item, info):
        '''当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败），
         item_completed() 方法将被调用'''
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

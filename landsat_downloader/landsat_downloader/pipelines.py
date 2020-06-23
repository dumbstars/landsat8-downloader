# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from scrapy import Request

class LandsatDownloaderPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'filename' : item.get('file_name')}) for x in item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        file_name = request.meta['filename'][0]

        return 'landsat-pds/' + str(file_name[10:13]) + '/' + str(file_name[13:16]) + '/' + file_name

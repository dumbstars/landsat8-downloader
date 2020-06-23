LIMIT = 100
FILE_PATH = '/home/shivam/data/college/PS 1/BISAG/data/'

path_p = 5
row_p = 6
date_p = 2
cloud_cover_p = 3
url_p = -1

import pickle
from datetime import datetime

def get_urls():

    try:
        with open(FILE_PATH + 'get_urls_log', 'rb') as fp:
            itemlist = pickle.load(fp)

    except FileNotFoundError as e:
        # print(e)
        itemlist = {}

    with open(FILE_PATH + 'scene_list', 'r') as reader:
        i = reader.readline()

        for i in reader.readlines():

            i = i.split(',')
            key = i[0][10:16]
            next_item = ([i[path_p], i[row_p], i[date_p], i[cloud_cover_p], i[url_p]])

            if key not in itemlist.keys():
                itemlist[key] = next_item
            else:
                date1 = itemlist[key][2]
                date2 = next_item[2]

                try:
                    date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
                except ValueError as e:
                    try:
                        date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        raise e

                try:
                    date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
                except ValueError as e:
                    try:
                        date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        raise e

                # condition for update
                # if datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') > datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f'):
                if date2 > date1:
                    itemlist[key] = next_item

    with open(FILE_PATH + 'get_urls_log', 'wb') as fp:
        pickle.dump(itemlist, fp)

    response = []

    for i in list(itemlist.values())[:LIMIT]:
        response.append(i[-1].strip())

    return response

# import time
# def get_urls():
#     time.sleep(100)
#     return ['https://s3-us-west-2.amazonaws.com/landsat-pds/c1/L8/149/039/LC08_L1TP_149039_20200606_20200606_01_RT/index.html']

import scrapy
from scrapy.loader import ItemLoader
from landsat_downloader.items import LandsatDownloaderItem

class LandsatDownloader(scrapy.Spider):
    name = 'landsat_downloader'

    start_urls = get_urls()
    print(start_urls)
    # start_urls = [
    #     'https://s3-us-west-2.amazonaws.com/landsat-pds/c1/L8/149/039/LC08_L1TP_149039_20200606_20200606_01_RT/index.html'
    # ]

    def parse(self, response):
        for link in response.xpath("//li/a"):
            loader = ItemLoader(item = LandsatDownloaderItem(), selector=link)
            link = link.xpath(".//@href").extract_first()

        # DOWNLOAD ONLY SMALL TEXT FILES
            if '.txt' in link:
                loader.add_value('file_name', link)
                link = response.urljoin(link)
                loader.add_value('file_urls', link)
                # loader.add_xpath('file_name', ".//text()")

                yield loader.load_item()

            # DOWNLOAD ALL FILES
            # loader.add_value('file_name', link)
            # link = response.urljoin(link)
            # loader.add_value('file_urls', link)
            # # loader.add_xpath('file_name', ".//text()")
            # yield loader.load_item()

        # DOWNLOAD SPECIFIC FILE
        # loader = ItemLoader(item = FileDownloadTutorialItem())
        # link = 'https://s3-us-west-2.amazonaws.com/landsat-pds/c1/L8/149/039/LC08_L1TP_149039_20170411_20170415_01_T1/LC08_L1TP_149039_20170411_20170415_01_T1_B8.TIF'
        # loader.add_value('file_name', link.split('/')[-1])
        # loader.add_value('file_urls', link)
        # yield loader.load_item()

# landsat8-downloader
After cloning this repository, set a few variables as follows

In landsat_downloader.py :-
1. at line 1 set LIMIT to the maximum number of scenes for which you want to download data
2. at line 2 set the file path where the scene_list file and get_urls_log file is stored

[scene_list file is available at https://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz and contains meta data about all the available satellite data]

[get_urls_log is a file created by this project which contains metdata about latest data available for every scene

In settings.py
1. at line 73, set the path for the downloads folder is located

python libraries used are :-
1. scrapy
2. pickle
3. datetime

to execute the project, execute the following command on terminal
cd landsat_downloader
ls
landsat_downloader scrapy.cfg
scrapy crawl landsat_downloader

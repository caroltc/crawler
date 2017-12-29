#!/usr/bin/env python
#-*-coding:utf-8-*-
import argparse
# import time
# import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#from scrapy.utils.log import configure_logging

from mycrawl.spiders.caol import CaolScrapy

#logging.basicConfig(
    #filename='/tmp/caoliu.log',
    #format='%(name)s %(levelname)s %(asctime)s: %(message)s',
    #datefmt="%Y-%m-%d %H:%M:%S",
    #level=logging.DEBUG
#)
#configure_logging({'LOG_STDOUT': True})

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_page', default=1, type=int)
    parser.add_argument('--cat_id', default='7', type=str)
    parser.add_argument('--cat_name', default='技术讨论区', type=str)
    parser.add_argument('--start_url', default='/thread0806.php?fid=7&search=&page=1', type=str)
    parser.add_argument('--url_keywords', default='htm_data', type=str)
    parser.add_argument('--sleep', default=3, type=int)
    parser.add_argument('--only_image', default=0, type=int)
    args = parser.parse_args()
    settings = get_project_settings()
    settings.set('MAX_PAGE', args.max_page, 'project')
    settings.set('CAT_ID', args.cat_id, 'project')
    settings.set('CAT_NAME', args.cat_name, 'project')
    settings.set('START_URL', args.start_url, 'project')
    settings.set('URL_KEYWORDS', args.url_keywords, 'project')
    settings.set('DOWNLOAD_DELAY', args.sleep, 'project')
    settings.set('ONLY_IMAGE', args.only_image, 'project')
    return settings

if __name__ == "__main__":
    settings = parse_args()
    crawler_process = CrawlerProcess(settings)
    crawler_process.crawl(CaolScrapy)
    crawler_process.start()
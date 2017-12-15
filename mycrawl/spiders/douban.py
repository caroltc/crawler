# -*- coding:utf-8 -*-
import scrapy

class DoubanScrapy(scrapy.Spider):
	name = "douban"
	allowed_domains = ["tieba.baidu.com"]
	start_urls = ["https://tieba.baidu.com/index.html"]
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理
	def parse(self, response):
		filename = "movie"
		with open("movie.txt", "wb") as f:
			f.write(response.body)
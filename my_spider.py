# encoding:utf-8

import re
import urllib.request
import urllib
from urllib import error
import queue
import threading
import os
from bs4 import BeautifulSoup
import sqlite3
import time


class MyRobot(threading.Thread):
	def __init__(self, num, url):
		threading.Thread.__init__(self)
		self.num = num
		self.url = url

	def save_data(self, data, filename):
		if not os.path.exists('blog'):
			blog_path = os.path.join(os.path.abspath('.'),'blog')
			os.mkdir(blog_path)
		try:
			fout = open('./blog/' + filename + '.html', 'wb')
			fout.write(data)
		except IOError as e:
			print('IO error:', e)

	def find_title(self,data):
		data = data.decode('gb2312')
		begin = data.find(r'<title') + 7
		end = data.find('\r\n',begin)
		title = data[begin:end]
		return title

	def db_save(self, data):
		conn = sqlite3.connect('petpet.db')
		c = conn.cursor()
		sql = "INSERT INTO articles (title, content, article_id, url, created_at) VALUES ('%s','%s', %s, '%s', %s)"%(data['title'], data['content'], data['article_id'], data['url'], time.time())

		c.execute(sql)
		conn.commit()

	def run(self):
		url = self.url + str(self.num) + '.html'
		try:
			res = urllib.request.urlopen(url)
			data = res.read()
			html=BeautifulSoup(data,'html.parser')
			#print(html.find_all('table')[9])
			# self.save_data(data,html.title.get_text())
			postData = {
				'title': html.title.get_text(),
				'content': html.find_all('table')[9],
				'article_id': self.num,
				'url': url
			}
			self.db_save(postData)
		except error.HTTPError as e:
			print(e.reason)

if __name__ == '__main__':
	for i in range(65):
		thread = MyRobot(i, 'http://www.weipet.cn/common/xunlian/xunlian-a')
		thread.start()
	for i in range(46):
		thread = MyRobot(i, 'http://www.weipet.cn/common/weiyang/weiyang-a')
		thread.start()
	for i in range(37):
		thread = MyRobot(i, 'http://www.weipet.cn/common/shengyu/shengyu-a')
		thread.start()
	for i in range(127):
		thread = MyRobot(i, 'http://www.weipet.cn/common/jibing/jibing-a')
		thread.start()

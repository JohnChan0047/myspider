from urllib.parse import urlencode, quote
import requests
import re
import json
import itertools
from multiprocessing import Pool, cpu_count
import os
import time
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775',
}
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}
char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(k): ord(v) for k, v in char_table.items()}


def buildUrls(word):# 得到网页的集合
	word = quote(word)
	url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={word}' \
          '&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={word}&face=0&istype=2&qc=&nc=1&fr=&pn={pn}'
	urls = (url.format(word=word, pn=x) for x in range(0, 660, 60))
	return urls


def changeUrl(url):
	for k, v in str_table.items():
		url = url.replace(k, v)
	url = url.translate(char_table)
	return url


def getImgUrl(url):
	req = requests.get(url, headers=headers, timeout=5)
	urls = [changeUrl(url) for url in re.findall(r'"objURL":"(.*?)"', req.text)]
	return urls


def DownImg(url, num):
	filename = str(num) + '.jpg'
	try:
		req = requests.get(url, headers=headers, timeout=5)
		if str(req.status_code)[0] == '4':
			print(req.status_code, '未能下载该图片', url)
			return False
	except Exception as e:
		print('抛出异常', url)
		print(e)
		return False
	with open(filename, 'wb') as f:
		f.write(req.content)
	return True


if __name__ == '__main__':
	os.chdir('D:\新建文件夹')
	word = input('输入关键词：')
	print(time.ctime())
	os.makedirs(word)
	os.chdir(word)
	urls = buildUrls(word)
	num = 0
	for url in urls:
		print('正在爬取：', url)
		for u in getImgUrl(url):
			if DownImg(u, num):
				print('正在下载第%s张' % num)
				num += 1
	print(time.ctime())
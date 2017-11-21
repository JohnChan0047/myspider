import requests
from bs4 import BeautifulSoup
import re
import json

# rl = "http://maoyan.com/board/4"
#
# payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"offset\"\r\n\r\n10\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.8",
    'connection': "keep-alive",
    'cookie': "uuid=1A6E888B4A4B29B16FBA1299108DBE9C34426156477D53072A53202D9C88716C; _lx_utm=; __mta=146511115.1498962"
            + "628552.1498964192311.1498964199972.8; _lxsdk_s=21e604472fa8d4dd6773cf29f31f%7C%7C19",
    'host': "maoyan.com",
    'ra-sid': "s_2367_r2x9ak474125_775",
    'ra-ver': "3.1.9",
    'referer': "http://maoyan.com/board",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4"
                  +" Safari/537.36 DOL/s_2367_r2x9ak474125_775",
    'cache-control': "no-cache",
    'postman-token': "2f51926f-9e6f-6f1a-8a33-1adbe7b6b16b"
    }
class Maoyantop100(object):
    # 定义属性：1、名字（猫眼电影TOP100）；2、100榜单初始化RUL
    def __init__(self, name, start_url):
        self.name = name
        self.start_url = start_url
    # 请求网页
    def get_page(self, url):
        response = requests.get(url, headers=headers)
        return response
    # 得到榜单页面的URL集合
    def url_list(self):
        url_list = [self.start_url]
        for x in range(1, 10):
            href = self.start_url + '?offset=' + str(x * 10)
            url_list.append(href)
        return url_list
    # 解析页面
    def parse_page(self, response):
        #html = self.get_page(self.start_url)
        pattern = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?data-src="(.*?)".*?title="(.*?)".*?class="star">'
                           + '(.*?)</p>.*?">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)
        items = re.findall(pattern, response.text)
        for item in items:
            yield {
                'index': item[0],
                'image': item[1],
                'title': item[2],
                'actors': item[3].strip()[3:],
                'time': item[4][5:],
                'score': item[5] + item[6]
            }
    def save(self):
        for url in self.url_list():
            items = self.parse_page(self.get_page(url))
            for item in items:
                print(item)
                with open(self.name + '.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
if __name__ == '__main__':
    url = 'http://maoyan.com/board/4'
    TOP100 = Maoyantop100('猫眼电影100榜单', url)
    TOP100.save()
    # print(TOP100.url_list())
    # print(TOP100.parse_page())
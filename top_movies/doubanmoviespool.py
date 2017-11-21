import requests
from bs4 import BeautifulSoup
import re
import json
from time import ctime
from multiprocessing import Pool,cpu_count

headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.8",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'cookie': "ll=\"118301\"; bid=p4lQAre2JSs; viewed=\"26284925\"; gr_user_id=80d7c185-d9bc-4e7e-bd7e-77425b8ddc9d; __yadk_uid=NPntdqLrdgljZ4fhkFF43oLIamh2bqyw; _vwo_uuid_v2=0026C6934C99BD7B9A8D371C134F608B|6069f53d237e2cf3f78ae1f3afab8235; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1498978412%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; ap=1; __utmt=1; _ga=GA1.2.1499433700.1497593226; _gid=GA1.2.1666588085.1498978451; as=\"https://movie.douban.com/subject_search?search_text=top250&cat=1002\"; ps=y; __utma=223695111.282678360.1497593226.1498962612.1498978412.4; __utmb=223695111.0.10.1498978412; __utmc=223695111; __utmz=223695111.1498103561.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_id.100001.4cf6=fb0557003c0f9c1f.1497593226.4.1498978569.1498962675.; _pk_ses.100001.4cf6=*; __utma=30149280.1499433700.1497593226.1498962612.1498978412.8; __utmb=30149280.4.9.1498978460946; __utmc=30149280; __utmz=30149280.1498897246.6.6.utmcsr=link.zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
    'host': "movie.douban.com",
    'ra-sid': "s_2367_r2x9ak474125_775",
    'ra-ver': "3.1.9",
    'referer': "https://movie.douban.com/chart",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775",
    'postman-token': "c1176654-a912-43d6-5524-fa0349280fe8"
    }
    # 请求网页
def get_page(url):
    response = requests.get(url, headers=headers)
    return response
# 得到榜单页面的URL集合
def url_list():
    start_url = 'https://movie.douban.com/top250'
    url_list = [start_url]
    for x in range(1, 10):
        href = start_url + '?start=' + str(x * 25) + '&filter='
        url_list.append(href)
    return url_list
# 解析页面
def parse_page(response):
    pattern = re.compile('<li>.*?class.*?(\d+)</em>.*?src="(.*?)".*?title">(.*?)</span>.*?class="">(.*?)<br>.*?(\d+).*?average">(.*?)</span>', re.S)
    items = re.findall(pattern, response.text)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actors': item[3].strip(),
            'time': item[4],
            'score': item[5]
        }

def main(url):
    items = parse_page(get_page(url))
    for item in items:
        print(item)
        with open('豆瓣电影.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    print(ctime())
    p = Pool(cpu_count())
    p.map(main, [url for url in url_list()])
    p.close()
    p.join()
    print(ctime())

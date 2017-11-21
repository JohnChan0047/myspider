# 爬取廖雪峰javascrip教程
# 2017-7-1
import requests
import re
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import pdfkit

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775',
}

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""
class Javasrcippdf(object):

    def __init__(self, name, start_url):
        self.name = name
        self.starturl = start_url
        self.f = 'http://www.liaoxuefeng.com'
# 网页响应
    def get_response(self, url):
        response = requests.get(url, headers=headers)
        return response
# 得到全部路径
    def get_urllist(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        ul = soup.find_all(class_="uk-nav uk-nav-side")[1]
        for li in ul.find_all('li'):
            href = li.a['href']
            url = ''.join([self.f, href])
            yield url

# 得到主体
    def get_body(self, response):
        soup = BeautifulSoup(response.content, 'lxml')

        title = soup.find('h4').get_text()
        title_tag = soup.new_tag('h1')
        title_tag.string = title
        center_tag = soup.new_tag('center')
        center_tag.insert(1, title_tag)

        body = soup.find(class_='x-wiki-content')
        body.insert(1, center_tag)
        html = str(body)
        pattern = '(<img .*?src=\")(.*?)(\")'

        def imgurl(m):
            if not m.group(2).startswith('http'):
                url = ''.join([m.group(1), self.f, m.group(2), m.group(3)])
                return url
            else:
                return ''.join([m.group(1), m.group(2), m.group(3)])

        html = re.compile(pattern).sub(imgurl, html)
        html = html_template.format(content=html)
        html = html.encode('utf-8')
        return html

#转换成PDF
    def get_pdf(self):
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        htmls = []
        url_list = self.get_urllist(self.get_response(self.starturl))
        for index, url in enumerate(url_list):
            html_name = '.'.join([str(index), 'html'])
            body = self.get_body(self.get_response(url))
            with open(html_name, 'wb') as f:
                f.write(body)
            htmls.append(html_name)
            print('创建了' + html_name + '超文本')
        pdfkit.from_file(htmls, self.name + '.pdf', options=options)


if __name__ == '__main__':
    os.chdir('E:\lianxi\廖雪峰javsrcippdf')
    start_url = 'http://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000'
    pdf = Javasrcippdf('javsrcippdf', start_url)
    print(pdf.get_pdf())
# 爬取《简明的Python》PDF
# 日期：2017-7-1
import pdfkit
import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775',
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

class Getpdf(object):

    #初始化属性：文件名，开始的URL
    def __init__(self, name, start_url):
        self.name = name
        self.start_url = start_url
        self.httphead = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.start_url)) + '/'
    #请求网页
    def Get_response(self, url):
        response = requests.get(url, headers=headers)
        return response
    #得到链接集合
    def Url_list(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        li_list = soup.find_all('li', class_='chapter')
        for li in li_list:
            href = li.a['href']
            url = self.httphead + href
            yield url
    #得到文章主体
    def Get_body(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        body = soup.find(class_='normal markdown-section')
        title = soup.find('h1').get_text().strip()
        # #制作HTML，把标题加入(后面发现不用中置标题)
        # title_tag = soup.new_tag('h1')
        # title_tag.string = title
        # center_tag = soup.new_tag('center')
        # center_tag.insert(1, title_tag)
        # body.insert(1, center_tag)
        #替换图片的地址
        html = str(body)
        pattern = '(<img.*?src=\")(.*?)(\")'
        def fun(m):
            if not m.group(2).startswith('http'):
                u = ''.join([m.group(1), self.httphead, m.group(2), m.group(3)])
                return u
            else:
                return ''.join([m.group(1), m.group(2), m.group(3)])
        html = re.compile(pattern).sub(fun, html)
        #把主体放入模板
        html = html_template.format(content=html)
        html = html.encode('utf-8')
        return html

    def Get_pdf(self):
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
        for index, url in enumerate(self.Url_list(self.Get_response(self.start_url))):
            html_name = '.'.join([str(index), 'html'])
            html = self.Get_body(self.Get_response(url))
            with open(html_name, 'wb') as f:
                f.write(html)
                print('正在创建' + html_name)
            htmls.append(html_name)
        pdfkit.from_file(htmls, self.name + '.pdf', options=options)
if __name__ == '__main__':
    os.chdir('E:\lianxi\简明的Python')
    start_url = 'https://bop.molun.net/'
    pdf = Getpdf('简明的Python', start_url)
    pdf.Get_pdf()
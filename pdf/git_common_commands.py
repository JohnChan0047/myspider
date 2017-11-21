# 阮一峰GIT常用命令
# 2017-7-1
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urlparse
import pdfkit

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775',
}
# HTML模板
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
class Get_pdf(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        # self.httphead = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.url))
    def get_response(self, url):
        response = requests.get(url, headers=headers)
        return response
    def get_body(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        body = soup.find(class_='asset-content entry-content')
        html = str(body)
        html = html_template.format(content=html)
        html = html.encode('utf-8')
        return html
    def run(self):
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
        html = self.get_body(self.get_response(self.url))
        name = self.name + '.html'
        with open(name, 'wb') as f:
            f.write(html)
        pdfkit.from_file(name, self.name + '.pdf', options=options)

if __name__ == '__main__':
    url = 'http://www.ruanyifeng.com/blog/2015/12/git-cheat-sheet.html'
    os.chdir('E:\资料文档PDF')
    pdf = Get_pdf('Git常用命令', url)
    pdf.run()

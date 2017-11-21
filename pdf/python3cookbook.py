import requests
import re
from bs4 import BeautifulSoup
import pdfkit
import os

url = 'http://python3-cookbook.readthedocs.io/zh_CN/latest/index.html'
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775",
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

def parse_url(url):
    response = requests.get(url, headers=headers)
    return response

def get_urllist(response):
    # url_list = []
    pattern = re.compile('<a class="reference internal" href="(.*?)"', re.S)
    hrefs = re.findall(pattern, response.text)
    for href in hrefs:
        u = 'http://python3-cookbook.readthedocs.io/zh_CN/latest/' + href
        yield u
        # print(u)
def get_body(response):
    soup = BeautifulSoup(response.content, 'lxml')
    body = soup.find('div', class_='section')
    html = str(body)
    pattern = '(<a.*?</a>)'
    html = re.compile(pattern).sub(':', html)
    html = html_template.format(content=html)
    html = html.encode('utf-8')
    return html
def save():

    # htmls = []
    for index, u in enumerate(get_urllist(parse_url(url))):
        name = str(index) + '.html'
        if not os.path.exists(name):
            html = get_body(parse_url(u))
            with open(name, 'wb') as f:
                print('开始创建：', name)
                f.write(html)
                print('创建完毕')
                f.close()
            # htmls.append(name)
        else:
            continue
    # pdfkit.from_file(htmls, 'python3cookbook.pdf', options=options)
    # html = get_body(parse_url(url))
    # with open('1.html', 'wb') as f:
    #     f.write(html)
    #     f.close()
    # pdfkit.from_file('1.html', '1.pdf', options=options)
def pdf():
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
    for i in range(310):
        name = str(i) + '.html'
        htmls.append(name)
    h1 = [htmls[0]]
    h2 = htmls[28:304]
    h3 = [htmls[308], htmls[309]]
    h = h1 + h2 + h3
    pdfkit.from_file(h, 'Python3cookbook.pdf', options=options)

def main():
    # get_urllist(parse_url(url))
    # print(get_body(parse_url(url)))
    os.chdir('E:\lianxi\新建文件夹 (3)')
    save()
    # print(get_body(parse_url(url)))
    # print(type(get_body(parse_url(url))))
if __name__ == '__main__':
    main()

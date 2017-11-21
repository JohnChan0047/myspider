import http.cookiejar
import requests
import re
import time
from PIL import Image
import json
headers = {
	'Referer': 'https://www.zhihu.com/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775',
}
session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')
try:
	session.cookies.load(ignore_discard=True)
	# print('成功加载Cookies')
except:
	print('未能加载Cookies')

def islogin():
	# 判断是否登录
	url = 'https://www.zhihu.com/settings/profile'
	r = session.get(url, headers=headers, allow_redirects=False)# allow_redirects requests参数，允许跳转设Ture，不允许设False
	if r.status_code == 200:
		# session.cookies.save()
		return True
	else:
		return False

def get_xsrf():
	# _xsrf 是登录时候提交的动态隐藏码
	url = 'https://www.zhihu.com/'
	req = session.get(url, headers=headers)
	html = req.text
	pattern = re.compile('name="_xsrf" value="(.*?)"', re.S)
	xsrf = re.findall(pattern, html)
	return xsrf[0]

def get_captcha():
	r = str(int(time.time()*1000)) #知乎规则为时间戳的1000倍取整
	url = 'https://www.zhihu.com/captcha.gif?r=' + r + '&type=login'
	cap = session.get(url, headers=headers)# 建立会话后，要用会话请求
	with open('captcha.jpg', 'wb') as f:
		f.write(cap.content)
		f.close()
	try:
		image = Image.open('captcha.jpg')
		image.show()
		image.close()
	except:
		print('请到文件夹中打开captcha.jpg并手动输入')
	captcha = input('请输入验证码：')
	return captcha

def login(name, password):# 登录函数
	_xsrf = get_xsrf()
	# headers['X - Requested - With'] = 'XMLHttpRequest'
	# headers['X - Xsrftoken']= 'da01940cbf8aa92b8400341d986d2ecf'
	# 根据用户名name判断登录方式是手机号登录还是邮箱登录，从而确定登录地址
	if '@' in name:
		print('邮箱登录')
		post_url = 'https://www.zhihu.com/login/email'
		post_data = {
			'email': name,
			'password': password,
			'_xsrf': _xsrf,
		}
		# req = session.post(post_url, data=post_data, headers=headers)
	else:
		if re.match(r'\d+$', name):
			print('手机号登录')
		else:
			print('账号输入有误，请重新输入')
		post_url = 'https://www.zhihu.com/login/phone_num'
		post_data = {
			'email': name,
			'password': password,
			'_xsrf': _xsrf,
		}
	req = session.post(post_url, data=post_data, headers=headers)
	code = req.json()
	if code['r'] == 1:# 如若登录失败，则尝试输入验证码，再判断登录信息
		post_data['captcha'] = get_captcha()
		req = session.post(post_url, data=post_data, headers=headers)
		code = req.json()
		print(code['msg'])
	session.cookies.save() # 保存cookies，下次直接使用



if __name__ == '__main__':
	if islogin():
		print('已经登录')
	else:
		name = input('请输入用户名：')
		password = input('请输入密码：')
		login(name, password)
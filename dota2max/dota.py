import requests
import re
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool, cpu_count
from time import ctime

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36 DOL/s_2367_r2x9ak474125_775",
}

def parse_url(url):
	req = requests.get(url, headers=headers)
	return req

def page_url(num):
	url = 'http://www.dotamax.com/player/match/' + str(num)
	req = parse_url(url)
	pattern = re.compile('<div class="nabtn pagerwidth.*?p=(\d+)')
	m = re.findall(pattern, str(req.text))[-1]
	url_list = []
	for i in range(1, int(m)+1):
		href = 'http://www.dotamax.com/player/match/' + str(num) + '/?skill=&ladder=&hero=-1&p=' + str(i)
		url_list.append(href)
	return url_list

def getmatchdata(url):

	req0 = parse_url(url)
	pattern = re.compile('<tr onclick="DoNav.*?href="(.*?)"><img.*?></img>(.*?)</a>.*?<td><font.*?>(.*?)</font>', re.S)
	matchs = re.findall(pattern, str(req0.text))
	for match in matchs:
		matchdata = {
			'play_id': str(156522248),
			'match_id': match[0][14:],
			'match_url': 'http://www.dotamax.com' + match[0],
			'hero': match[1].strip(),
			'result': match[2]
		}
		req = parse_url(matchdata['match_url'])
		pattern1 = re.compile('<table class="match-detail-info new-box".*?'
							  '<td class="fromnow".*?</td><td>(.*?)</td>'
							  '<td>(.*?)</td><td>(.*?)</td>.*?<font.*?>(.*?)</font>.*?<td>(.*?)</td>', re.S)
		top_data = re.findall(pattern1, str(req.text))[0]
		matchdata['Time'] = top_data[0]
		matchdata['Area'] = top_data[1]
		matchdata['Fb_time'] = top_data[2]
		matchdata['Match_level'] = top_data[3]
		matchdata['Mode'] = top_data[4]

		soup = BeautifulSoup(req.text, 'lxml').find('div', class_="main-shadow-box").find('div',
																						  style="margin-top: 20px;width:100%;margin-left: auto;margin-right:auto;")
		pattern2 = re.compile('<p.*?>(.*?)</p><table.*?>(.*?)</table>', re.S)
		fdata = re.findall(pattern2, str(soup))
		for i in fdata:
			for x in i:
				if matchdata['play_id'] in x:
					matchdata['Formation'] = i[0].strip()[:2]

		pattern3 = re.compile('<tr.*?>.*?href="/player/detail/156522248".*?<a.*?><img.*?>(.*?)</a>.*?'
							  '<div.*?>(.*?)</div>.*?<div.*?>(.*?)</div>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>'
							  '<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>'
							  '(.*?)</td>.*?<div.*?>(.*?)</div><div.*?>(.*?)</div>.*?</tr>', re.S)

		mid_data = re.findall(pattern3, str(soup))[0]
		matchdata['Play_level'] = mid_data[0].strip()
		if 'MVP' in mid_data[1]:
			matchdata['MVP'] = 'YES'
		else:
			matchdata['MVP'] = 'NO'
		matchdata['KDA'] = mid_data[2]
		matchdata['K/D/A'] = mid_data[3].strip()
		matchdata['War_rate'] = mid_data[4]
		matchdata['Damage_rate'] = mid_data[5]
		matchdata['Damage_number'] = mid_data[6]
		matchdata['Positive/Inverse'] = mid_data[7]
		matchdata['XPM'] = mid_data[8]
		matchdata['GPM'] = mid_data[9]
		matchdata['Building_damage'] = mid_data[10]
		matchdata['Heroic_healing'] = mid_data[11]
		pattern3 = re.compile('<a href="/item/detail/(.*?)"', re.S)
		all_backpack = re.findall(pattern3, mid_data[12])
		matchdata['all_backpack'] = all_backpack
		if mid_data[13]:
			extra_backpack = re.findall(pattern3, mid_data[13])
		else:
			extra_backpack = ''
		matchdata['extra_backpack'] = extra_backpack
		with open(url[-2:]+'.txt', 'a', encoding='utf-8') as f:
			f.write(json.dumps(matchdata, ensure_ascii=False) + '\n')
		print(matchdata)

def main(url):
	getmatchdata(url)

if __name__ == '__main__':
	num = input("请输入玩家ID：")
	print(ctime())
	url_list = page_url(num)
	with Pool(cpu_count()) as pool:
		pool.map(main, url_list)
		pool.close()
		pool.join()
	print(ctime())
	# for url in url_list:
	# 	main(url)



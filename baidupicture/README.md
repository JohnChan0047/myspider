# 说明

## 1、百度图片对图片的真实地址进行了加密，通过changeUrl(url)和getImgUrl(url)对图片进行解密获取图片的真是地址。
## 2、下载的图片放在D盘新建文件夹内。
## 3、在buildUrls(word)函数中，url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={word}&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={word}&face=0&istype=2&qc=&nc=1&fr=&pn={pn}'  
ct=201326592表示时间戳，work代表关键词， pn代表每页的图片数。

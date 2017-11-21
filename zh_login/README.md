spider_login  
爬虫网站登录记录：跟着https://github.com/xchaoinfo/fuck-login 这位大神学。  
一、知乎  
  1、_xsrf 是登录时候提交的动态隐藏码；  
  2、知乎验证码：url = "https://www.zhihu.com/captcha.gif?r=1499823459191&amp;type=login&amp;lang=cn"  
          r=1499823459191：r是时间戳time.time(),根据时间确定验证码；  
          type=login：类型为登录；  
          lang=cn：中文验证码（点击倒立字体）lang=en：英文验证码（直接输入，简单方便，采用此种）；  
          &amp：？暂时不知有什么用，删除了也不影响显示；  
   3、建立会话后，需要用会话请求：例如cap = session.get(url, headers=headers)与cap = requests.get(url, headers=headers)得到的同；

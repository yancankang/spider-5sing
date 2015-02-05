# -*- coding=utf-8 -*-
import urllib.request
import http.cookiejar
import urllib.parse
import urllib
import time
import globalValues
from html_producer import producer
from html_consumer import consumer
# 开启debug模式
# HTTPConnection.debuglevel=1
# 处理消息头和消息体，消息体需要编码为二进制，消息头utf-8
# 十分钟访问了1680个页面
indexUrl = 'http://5sing.kugou.com/login/'

# http://5sing.kugou.com/my
loginData = {'RefUrl': 'http://5sing.kugou.com/index.html', 'txtUserName': 'ycktest1', 'txtPassword': 'ycktest1',
             'txtCheckCode': '验证码'}
loginData = urllib.parse.urlencode(loginData).encode('utf-8')
tempData = {'user': 'admin'}
tempData = urllib.parse.urlencode(tempData).encode('utf-8')

# header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept-Language':'zh-CN,zh;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'}
headers = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
           ('Accept-Language', 'zh-CN,zh;q=0.8'), ('User-Agent',
                                                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36')]


# 增加cookie信息
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
opener.addheaders = headers
urllib.request.install_opener(opener)

# 初始化访问过的集合和待访问的url队列


def login():
    '''
    登陆
    :return:
    '''
    openingUrl = globalValues.urlQueue.popleft()
    globalValues.logger.info('正在访问网页：%s' % (openingUrl))
    request = urllib.request.Request(openingUrl, loginData)
    response = urllib.request.urlopen(request)
    globalValues.visited.append(openingUrl)
    html = response.read().decode('utf-8', 'ignore')

    for urlChild in globalValues.linkRe.findall(html):
        urlChild not in globalValues.visited and urlChild not in globalValues.urlQueue and globalValues.urlQueue.append(urlChild)

if __name__ == '__main__':
    # 加入主页
    globalValues.urlQueue.append(indexUrl)
    login()
    for i in range(20):
        producer('producer'+str(i)).start()

    time.sleep(10)

    for i in range(2):
        consumer('consumer'+str(i)).start()
'''
    while globalValues.urlQueue:
        html = globalValues.openUrl()
        if (html == None):
            continue
        writeSongMsg(html)
    print(globalValues.success)
    '''
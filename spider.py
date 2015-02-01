# -*- coding=utf-8 -*-
import urllib.request
import http.cookiejar
import urllib.parse
import urllib
from http.client import HTTPConnection
from collections import deque
import re

# 开启debug模式
#HTTPConnection.debuglevel=1
#处理消息头和消息体，消息体需要编码为二进制，消息头utf-8
indexUrl = 'http://5sing.kugou.com/login/'

#http://5sing.kugou.com/my
loginData = {'RefUrl': 'http://5sing.kugou.com/index.html', 'txtUserName': 'a674810893', 'txtPassword': 'a7921541',
             'txtCheckCode': '验证码'}
loginData = urllib.parse.urlencode(loginData).encode('utf-8')
tempData = {'user': 'admin'}
tempData = urllib.parse.urlencode(tempData).encode('utf-8')

#header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#'Accept-Language':'zh-CN,zh;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'}
headers = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
           ('Accept-Language', 'zh-CN,zh;q=0.8'), ('User-Agent',
                                                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36')]


#增加cookie信息
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
opener.addheaders = headers
urllib.request.install_opener(opener)

#初始化访问过的集合和待访问的url队列
visited = set()
urlQueue = deque()
count = 0

#加入主页
urlQueue.append(indexUrl)

linkRe = re.compile('href="(.+?.html)"')


def openUrl():
    global count
    openingUrl = urlQueue.popleft()
    print('%d.正在访问网页：%s.' % (count, openingUrl))

    try:
        request = urllib.request.Request(openingUrl)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8', 'ignore')  #.encode('utf-8','ignore').decode('utf-8')
    except Exception as e:
        print('%s 抓取失败' % (openingUrl))
        print(e)
        return

    for urlChild in linkRe.findall(html):
       urlChild not in visited and urlQueue.append(urlChild)
    count += 1

    with open('temp/' + str(count) + '.html', 'w', encoding='utf-8') as file:
        file.write(html)

    with open('result.txt',encoding='utf-8',errors='ignore',mode='a') as result_file:

        result_file.write(getWord('演唱：'))
        result_file.write(getWord('作词：'))
        result_file.write(getWord('作曲：'))
        result_file.write(getWord('编曲：'))

def buildMusicMsg(html):
    singer=

#进行登录
def login():
    openingUrl = urlQueue.popleft()
    print('正在访问网页：%s' % (openingUrl))
    request = urllib.request.Request(openingUrl, loginData)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8', 'ignore')

    for urlChild in linkRe.findall(html):
        urlQueue.append(urlChild)


def getWord(word, html):
    start = html.find(word)
    word_start = html.find('title=\"', start, start + 500) + 7
    word_end = html.find('\"', word_start, word_start + 50)
    return html[word_start:word_end]


login()

while urlQueue:
    openUrl()

print(count)







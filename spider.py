# -*- coding=utf-8 -*-
import urllib.request
import http.cookiejar
import urllib.parse
import urllib
from http.client import HTTPConnection
from collections import deque
import re
import os
import globalValues
# 开启debug模式
# HTTPConnection.debuglevel=1
# 处理消息头和消息体，消息体需要编码为二进制，消息头utf-8
indexUrl = 'http://5sing.kugou.com/login/'

# http://5sing.kugou.com/my
loginData = {'RefUrl': 'http://5sing.kugou.com/index.html', 'txtUserName': 'ycktest1', 'txtPassword': 'ycktest1',
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
        response = urllib.request.urlopen(request, timeout=10)
        html = response.read().decode('utf-8', 'ignore')
    except Exception as e:
        print('%s 抓取失败' % (openingUrl))
        print(e)
        return
    finally:
        visited.add(openingUrl)

    for urlChild in linkRe.findall(html):
        urlChild not in visited and urlQueue.append(urlChild)
    count += 1
    # with open('temp/' + str(count) + '.html', 'w', encoding='utf-8') as file:
    #    file.write(html)
    return html





def buildSongMsg(html):
    '''
    从抓取的网页中，提取有用信息，并且拼接为一行
    :param html:
    :return:
    '''
    try:
        return {x: getWord(x, html) for x in globalValues.keys[getSongType(html)]}
    except:
        return None


def login():
    '''
    登陆
    :return:
    '''
    openingUrl = urlQueue.popleft()
    print('正在访问网页：%s' % (openingUrl))
    request = urllib.request.Request(openingUrl, loginData)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8', 'ignore')

    for urlChild in linkRe.findall(html):
        urlQueue.append(urlChild)


def getWord(word, html):
    '''
    获取演唱，作词等信息
    :return 演唱等
    '''
    start = html.find(word)
    word_start = html.find('title=\"', start, start + 500) + 7
    word_end = html.find('\"', word_start, word_start + 50)
    if start == -1 or word_start == 6 or word_end == -1:
        word_end = html.find('</a>', start, start + 500)
        word_start = html.rfind('>', 0, word_end) + 1
    if start == -1 or word_start == -1 or word_end == -1:
        word = None
    else:
        word = html[word_start:word_end]
    return word


def getSongType(html):
    if html.find('原唱：') != -1 and html.find('演唱：') != -1:
        return 0
    elif html.find('混缩：') != -1 and html.find('演唱：') != -1:
        return 1


def getSongName(html):
    start = html.find('class=\"view_tit\"')
    word_start = html.find('<h1>', start, start + 500) + 4
    word_end = html.find('</h1>', start, start + 500)
    if start == -1 or word_start == 3 or word_end == -1:
        return None
    else:
        return html[word_start:word_end]


def writeSongMsg(html):
    songName = getSongName(html)
    msg = buildSongMsg(html)
    if songName and msg:
        globalValues.SONG_MSG_BUFFER = globalValues.SONG_MSG_BUFFER + songName + msg.__str__() + '\n\n'
        if len(globalValues.SONG_MSG_BUFFER) > globalValues.BUFFER_SIZE:
            filePath = 'result/songs' + str(globalValues.FILE_INDEX) + '.txt'
            with open(filePath, encoding='utf-8', errors='ignore', mode='a') as result_file:
                print('写入歌曲信息')
                result_file.write(globalValues.SONG_MSG_BUFFER)
                globalValues.SONG_MSG_BUFFER = ''
            if (os.path.getsize(filePath) > globalValues.FILE_SIZE):
                globalValues.FILE_INDEX += 1


if __name__=='__main__':
    login()

    while urlQueue:
        html = openUrl()
        if (html == None):
            continue
        writeSongMsg(html)

    print(count)







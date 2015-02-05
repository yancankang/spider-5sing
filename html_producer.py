# -*- coding=utf-8 -*-
__author__ = 'yancankang'
import urllib.request
import urllib,re
import threading

import globalValues


class producer(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name
        #正则表达式
        self.linkRe = re.compile('href="(.+?.html)"')
        pass

    def run(self):
        globalValues.COUNTER.success=0
        globalValues.COUNTER.fail=0
        globalValues.COUNTER.song_page_count=0
        while(globalValues.urlQueue):
            self.openUrl()

    def openUrl(self):
        openingUrl = globalValues.urlQueue.popleft()
        globalValues.logger.info('线程'+self.name+': %d.正在访问网页：%s.' % (globalValues.COUNTER.success, openingUrl))
        try:
            request = urllib.request.Request(openingUrl)
            response = urllib.request.urlopen(request, timeout=10)
            html = response.read().decode('utf-8', 'ignore')

            globalValues.htmlQueue.append(html)

            globalValues.COUNTER.success += 1
        except Exception as e:
            globalValues.logger.info('%s 抓取失败' % (openingUrl))
            globalValues.logger.info(e)
            globalValues.COUNTER.fail+=1
            return
        finally:
            globalValues.visited.append(openingUrl)
        for urlChild in self.linkRe.findall(html):
            urlChild not in globalValues.visited and urlChild not in globalValues.urlQueue and globalValues.urlQueue.append(urlChild)
        globalValues.logger.debug(self.name+'*************urlQueue:'+str(len(globalValues.urlQueue)))
        globalValues.logger.debug(self.name+'*************htmlQueue:'+str(len(globalValues.htmlQueue)))
        # globalValues.logger.info('************'+str(len(set(globalValues.urlQueue))))


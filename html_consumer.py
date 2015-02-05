__author__ = 'yancankang'
import threading
import globalValues
import os
class consumer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        globalValues.COUNTER.song_page_count=0
        while True:
            if globalValues.htmlQueue:
                globalValues.logger.debug(self.name+'------------:htmlQueue剩余：'+str(len(globalValues.htmlQueue))+'访问过得页面:'+str(len(globalValues.visited))+'成功处理的有效页面：'+str(globalValues.COUNTER.song_page_count))
                self.writeSongMsg(globalValues.htmlQueue.popleft())

    def buildSongMsg(self,html):
        '''
        从抓取的网页中，提取有用信息，并且拼接为一行
        :param html:
        :return:
        '''
        try:
            return {x: self.getWord(x, html) for x in globalValues.KEYS[self.getSongType(html)]}
        except:
            return None

    def getWord(self,word,html):

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


    def getSongType(self,html):
        if html.find('原唱：') != -1 and html.find('演唱：') != -1:
            return 0
        elif html.find('混缩：') != -1 and html.find('演唱：') != -1:
            return 1


    def getSongName(self,html):
        start = html.find('class=\"view_tit\"')
        word_start = html.find('<h1>', start, start + 500) + 4
        word_end = html.find('</h1>', start, start + 500)
        if start == -1 or word_start == 3 or word_end == -1:
            return None
        else:
            return html[word_start:word_end]


    def writeSongMsg(self,html):
        songName = self.getSongName(html)
        msg = self.buildSongMsg(html)
        if songName and msg:
            globalValues.SONG_MSG_BUFFER = globalValues.SONG_MSG_BUFFER + songName + msg.__str__() + '\n\n'
            globalValues.COUNTER.song_page_count += 1
            if len(globalValues.SONG_MSG_BUFFER) > globalValues.BUFFER_SIZE:
                filePath = 'result/songs' + str(globalValues.FILE_INDEX) + '.txt'
                with open(filePath, encoding='utf-8', errors='ignore', mode='a') as result_file:
                    globalValues.logger.info('写入歌曲信息,正确的歌曲页面数：' + str(globalValues.COUNTER.song_page_count))
                    result_file.write(globalValues.SONG_MSG_BUFFER)
                    globalValues.SONG_MSG_BUFFER = ''
                if (os.path.getsize(filePath) > globalValues.FILE_SIZE):
                    globalValues.FILE_INDEX += 1
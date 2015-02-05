__author__ = 'yancankang'
from collections import deque
import re
import queue
import threading
import logging
# 写文件缓存
SONG_MSG_BUFFER = ''
# 缓冲区大小
BUFFER_SIZE = 10000
# 文件的索引
FILE_INDEX = 0
# 一个文件的大小100,000,000.0
FILE_SIZE = 100000000.0
# 提取信息的关键字
KEYS = (('演唱：', '原唱：'), ('演唱：', '作词：', '作曲：', '编曲：'))

COUNTER=threading.local()
# 访问成功的网页的个数
COUNTER.success = 0
# 访问失败的网页个数
COUNTER.fail=0
# 正确的歌曲页面数
COUNTER.song_page_count=0
# 待访问的url队列(线程安全)
urlQueue = deque()
#访问过的url集合
visited = deque()
# 待处理的html队列
htmlQueue=deque()
#正则表达式
linkRe = re.compile('href="(.+?.html)"')



#create logger
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -%(message)s")
#add formatter to ch
ch.setFormatter(formatter)
#add ch to logger
logger.addHandler(ch)
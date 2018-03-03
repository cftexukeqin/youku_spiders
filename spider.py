import requests
from bs4 import BeautifulSoup as bs
import threading
from datetime import datetime

#定义两个列表，分别存放url和获取到的数据
TOTAL_URL_LIST = []
INFO_LIST = []
#线程锁
gLock = threading.Lock()

#接受用户输入的地址
input_url = input('请输入视频空间地址：')
input_page = input('請輸入最大頁數：')
print('Spidering...')
# 创建所有的urls,添加到列表http://i.youku.com/i/UMzYwMzY5MzA0OA==/videos?spm=a2hzp.8253869.0.0
BASE_URL = input_url + "&order=1&page={}"
for i in range(1, int(input_page) + 1):
    per_page = BASE_URL.format(i)
    TOTAL_URL_LIST.append(per_page)

#生产者，获取所有页的信息
def mythread():
    while True:
        gLock.acquire()
        #判断列表是否为空
        if len(TOTAL_URL_LIST) == 0:
            gLock.release()
            break
        else:
            gLock.release()
            page_url = TOTAL_URL_LIST.pop()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Host': 'i.youku.com'
            }
            res = requests.get(page_url, headers=headers)
            soup = bs(res.text, 'lxml')
            titles = soup.select('.v-meta-title a')
            #获取到的信息添加到信息列表
            gLock.acquire()
            for title in titles:
                try:
                    with open('video.txt','a+',encoding='utf-8') as df:
                        df.write(title['title']+'-->>http'+title['href']+'\n')
                except:
                    print('写入文件出错')
            gLock.release()


def main():
    for i in range(4):
        th = threading.Thread(target=mythread)
        th.start()

if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    last_time = (end_time - start_time).total_seconds()
    print('用时%s秒' % last_time)





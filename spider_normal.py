import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


#生产者，获取所有页的信息
def get_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'i.youku.com'
    }
    res = requests.get(url, headers=headers)
    soup = bs(res.text, 'lxml')
    titles = soup.select('.v-meta-title a')
    #获取到的信息添加到信息列表
    for title in titles:
        with open('video1.txt','a+',encoding='utf-8') as df:
            df.write(title['title']+'-->>http'+title['href']+'\n')

def main():
    # 接受用户输入的地址
    input_url = input('请输入视频空间地址：')
    input_page = input('請輸入最大頁數：')
    print('Spidering...')
    # 创建所有的urls,添加到列表
    BASE_URL = input_url + "&order=1&page={}"
    for i in range(1, int(input_page)+1):
        per_page = BASE_URL.format(i)
        get_info(per_page)

if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    last_time = (end_time - start_time).total_seconds()
    print('用时%s秒' % last_time)



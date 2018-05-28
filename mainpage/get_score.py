import requests
import datetime


def get_level(bookname):
    header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'api.douban.com'
        }
    get_url = 'https://api.douban.com/v2/book/search?q=%s' % bookname #通过豆瓣API搜索图书，获取评分
    content = requests.get(get_url, headers=header).json()
    try:
        score = content['books'][0]['rating']['average']
    except IndexError:
        score = 0.0
    return score


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print(get_level('asdasf'))
    end_time = datetime.datetime.now()
    print('time:%s' % (end_time-start_time))

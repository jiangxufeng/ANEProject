import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import datetime


#获取豆瓣评分
# def get_book_url(bookname):
#     header = {
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Host': 'book.douban.com'
#     }
#     get_url = 'https://book.douban.com/j/subject_suggest?q=%s' % bookname   # 获取搜索框智能匹配返回的json数据
#     content = requests.get(get_url, headers=header).json()  # 获取该图书在豆瓣网的具体url
#     book_url = content[0]['url']
#     book_content = requests.get(book_url, headers=header).text
# #   使用Beautifulsoup 进行查找，速度慢于使用lxml
# #   print(book_content.text)
# #     soup = bs(book_content, 'lxml')
# #     score = soup.find(attrs={'class': 'rating_num'}).text.lstrip().rstrip()
# #     print(score)
# #   使用lxml进行查找
#     tree = html.fromstring(book_content)
#     score = tree.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0].lstrip().rstrip()
#     print(score)
def get_book_score(bookname):
    header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'api.douban.com'
        }
    get_url = 'https://api.douban.com/v2/book/search?q=%s' % bookname #通过豆瓣API搜索图书，获取评分
    #print(get_url)
    content = requests.get(get_url, headers=header).json()
   # print(content)
    score = content['books'][0]['rating']['average']
  #  print(score)
    return score


if __name__ == '__main__':
    #start_time = datetime.datetime.now()
    get_book_score('百年孤独')
   # end_time = datetime.datetime.now()
   # print('time:%s' %(end_time-start_time))

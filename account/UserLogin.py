import requests
from rewrite.exception import ServerWrong

headers = {
    'Connection': 'keep-alive',
    'Host': 'seat.lib.whu.edu.cn:8443',
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch'
}


def Userlogin(username, password):
    url3 = 'https://seat.lib.whu.edu.cn:8443/rest/auth?username=%s&password=%s' % (username, password)
    proxy = {
        'http': None,
        'https': None,
    }
    content = requests.get(url3, headers=headers, proxies=proxy).json()
    try:
        result = content['status']
    except KeyError:
        raise ServerWrong
    if result == 'success':
        url_2 = 'https://seat.lib.whu.edu.cn:8443/rest/v2/user?token=%s' % (content['data']['token'])
        json_2 = requests.get(url_2, headers=headers, proxies=proxy).json()
        return json_2['data']['name']
    else:
        return False

# coding=utf-8
"""
版本六
添加功能：使用抓包得到的cookie，模拟登入知乎，向知乎提交关键词，返回搜索到的内容

知乎搜索接口：'https://www.zhihu.com/search'
要添加的关键字{'type': 'content', 'q': u'爬虫'}
读写文件用字节流
"""
import requests
from Cookie import SimpleCookie


def get_headers(filename):
    """将文件中的头信息转换为字典格式"""
    headers = {}
    with open(filename, 'r') as fp:
        # 每一行以:为分隔符，1为分割次数
        for line in fp.readlines():
            name, values = line.split(':', 1)
            headers[name.strip()] = values.strip()
    return headers


def get_cookie(cookie_filename):
    """cookie_filename是一个从抓包获取的cookie字符串文件"""
    with open(cookie_filename, 'r') as fc:
        raw_cookie = fc.read()
    # raw_cookie是一个cookie字符串，需要将它变成一个字典类型
    cookie = SimpleCookie(raw_cookie)
    cookies_dict = dict([(c, cookie[c].value) for c in cookie])
    return cookies_dict

if __name__ == '__main__':
    filename = 'headers_raw.txt'
    cookie_filename = 'cookie.txt'
    # 知乎搜索界面
    url = 'https://www.zhihu.com/search'
    headers = get_headers(filename)
    keywords = {'type': 'content', 'q': u'爬虫'}
    cookie_dict = get_cookie(cookie_filename)

    session = requests.Session()
    result = session.get(url, headers=headers, cookies=cookie_dict, params=keywords)
    result.encoding = 'utf-8'
    print result.status_code
    with open('spider.html', 'wb') as f1:
        f1.write(result.content)



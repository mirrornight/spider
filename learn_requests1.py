# coding=utf-8
'''
第一个版本
功能：访问一个url，获取页面信息，捕获异常
'''
import requests

def get_HTML_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text  # unicode
    except:
        return u'产生异常'
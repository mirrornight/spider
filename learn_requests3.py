# coding=utf-8
'''
版本三
添加功能：向知乎提交关键词，返回搜索到的内容

知乎搜索接口：'https://www.zhihu.com/search'
要添加的关键字{'type': 'content', 'q': u'妹纸'}
'''
import requests

def get_headers(filename):
    '''将文件中的头信息转换为字典格式'''
    headers = {}
    with open(filename, 'r') as fp:
        # 每一行以:为分隔符，1为分割次数
        for line in fp.readlines():
            name, values = line.split(':', 1)
            headers[name.strip()] = values.strip()
    return headers

def get_HTML_text(url, headers, params):
    '''输入url和对应的头信息，返回页面内容'''
    try:
        # 增加关键字params
        r = requests.get(url, headers = headers, timeout = 10, params = params)
        r.raise_for_status() # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        # 查看发送到服务器的请求的头部
        # print r.request.headers
        # 查看发送知乎的url
        print r.request.url
        return r.text # unicode
    except requests.HTTPError, e:
        print u'捕获http异常'
    except requests.ConnectionError, e:
        print u'捕获连接异常'
    except requests.Timeout, e:
        print u'捕获超时异常'
    except:
        print u'其他异常捕获'

if __name__ == '__main__':
    filename = 'headers_raw.txt'
    headers = get_headers(filename)
    # 知乎搜索界面
    url =  'https://www.zhihu.com/search'
    keywords = {'type': 'content', 'q': u'妹纸'}
    print get_HTML_text(url, headers, keywords)[:1000]


# coding=utf-8
'''
版本二：
发给服务器的请求中添加了头信息，同时添加了一个get_headers，
将文件中包含的头信息提取出来放到字典中
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

def get_HTML_text(url, headers):
    '''输入url和对应的头信息，返回页面内容'''
    try:
        # 增加头部信息
        r = requests.get(url, headers = headers, timeout = 10)
        r.raise_for_status() # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        # 查看发送到服务器的请求的头部
        # print r.request.headers
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
    # url = 'https://www.zhihu.com'
    # 404页面测试，引发httperror
    url = 'https://www.zhihu.com/question/19600828'  # [这是一个404页面]
    print get_HTML_text(url, headers)[:1000]
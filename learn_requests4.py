# coding=utf-8
'''
版本四

下载图片的关键
1.读取文件的二进制形式
r.content
2.写二进制
open('filename.jpg', 'wb')
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

def get_HTML_text(url):
    try:
        r = requests.get(url, timeout = 10)
        r.raise_for_status() # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        # 返回文件的二进制
        return r.content # str
    except requests.HTTPError, e:
        print u'捕获http异常'
    except requests.ConnectionError, e:
        print u'捕获连接异常'
    except requests.Timeout, e:
        print u'捕获超时异常'
    except:
        print u'其他异常捕获'

if __name__ == '__main__':
    #filename = 'headers_raw.txt'
    #headers = get_headers(filename)
    # 图片链接
    url =  'http://konachan.net/sample/143331e8c7b001b41350e7e84782d12d/Konachan.com%20-%20250579%20sample.jpg'
    picture_name = url.split('/')[-1]
    print picture
    with open(picture_name, 'wb') as f:
        f.write(get_HTML_text(url))



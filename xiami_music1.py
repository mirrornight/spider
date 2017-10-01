# coding=utf-8
'''
版本一，输入虾米歌曲id，下载歌曲到本地(推荐一首id：1796739355)
难点：
1.找到歌曲xml文档
2.解析下载地址
'''
import requests
from bs4 import BeautifulSoup
import urllib2

# 根据播放地址是http://www.xiami.com/song/play?ids=/song/playlist/id/12372/type/1 获取歌曲XML文档路径。
# 即ids参数即为歌曲的XML文档路径，即http://www.xiami.com/song/playlist/id/12372
# id 后面跟歌曲的id号，例如1796739355
music_id = raw_input(u'输入歌曲的id号：')
url = 'http://www.xiami.com/song/playlist/id/' + music_id
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
r = requests.get(url, headers=headers)
xml_doc = r.content

# 解析xml获取歌曲的名称，id号，源文件
soup = BeautifulSoup(xml_doc, ["lxml", "xml"])
song_id = soup.find(name='songId').string
song_name = soup.find(name='songName').string
song_location = soup.find(name='location').string


def decrypt(s):
    """
    这个歌曲源文件的url是加密的
    参考网上资料，知道这个经过凯撒阵列算法加密
    1.先解析成正确的序列，通过从上到下，从左到右读取，可以看到是http开头的
    7
    h%1m2F11519845pt37EE63bc54
    t22iF28%E92%783hD4%-6a1b1d
    tF8.81%22%7578%_135%dd63%
    p%.n115F42%E463k51E51%a%5
    %2xe1%E21F5479Fe%6-E45a5E
    3Fit%58131E_6.ay5%%-fEcE1
    Ama%2E1%77115mu%E55ab6596
    2.使用urllib2.unquote将'%xx'用对应的单个字符替换
    3.将'^'使用'0'替换，从而得到正确的下载地址
    """
    new_s = s[1:]
    length = len(new_s)  # 去除第一个字符后的长度
    r_num = int(s[0])  # 行数
    a = length / r_num  # 一行最少有a个字符
    b = length % r_num  # a+1个字符有b行
    # c_num = [a+1]*b + [a]*(r_num-b)  计算出每行多少个字符
    output = ''
    for i in xrange(length):
        y = i % r_num  # 加入output字符的所在行
        x = i / r_num  # 加入output字符的所在列
        if y <= b:
            p = y * (a + 1) + x
        else:
            p = b * (a + 1) + (y - b) * a + x
        output += new_s[p]
    return urllib2.unquote(output).replace('^', '0')

download_url = decrypt(song_location)
print download_url
r = requests.get(download_url, headers=headers)
with open('%s.mp3' % song_name, 'wb') as f:
    print u'正在下载 %s' % song_name
    f.write(r.content)
    print u'下载完成 %s' % song_name






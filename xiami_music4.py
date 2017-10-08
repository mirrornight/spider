# coding=utf-8
"""
登入虾米
下载猜你喜欢歌曲
下载速度与网速有关
"""

import requests
import re
import multiprocessing
import urllib2

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
}


def get_informations(login_url):
    r = session.get(login_url, headers=headers)
    html_doc = r.content
    token = re.search(r'<input type="hidden" name="_xiamitoken" value="(.+?)" />', html_doc).group(1)
    done_url = re.search(r'<input type="hidden" value="(.+?)" name="done">', html_doc).group(1)
    return token, done_url


def login(token, done_url, account_number, password, post_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'https://login.xiami.com/member/login',
    }
    data = {
        '_xiamitoken': token,
        'done': done_url,
        'verifycode': '',
        'account': account_number,
        'pw': password,
        'submit': u'登 录',
    }
    session.post(post_url, headers=headers, data=data)


def decrypt(s):
    """
    将歌曲源文件的url解密, 返回字符串类型
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


def download_song(q):
    """
    下载歌曲
    """
    while True:
        item = q.get()
        song_name = item[0].decode('utf-8')
        song_durl = decrypt(item[1])
        r = session.get(song_durl, headers=headers)
        print u'正在下载' + '%s' % song_name
        try:
            with open('%s.mp3' % song_name, 'wb') as f:
                f.write(r.content)
        except IOError, e:
            print e
        finally:
            q.task_done()


if __name__ == '__main__':
    # 1.登入
    login_url = 'https://login.xiami.com/member/login'
    post_url = 'https://login.xiami.com/passport/login'
    # 输入账号和密码
    account_number = raw_input('input your account\n')
    password = raw_input('input your password\n')
    # 将cookie存入会话
    token, done_url = get_informations(login_url)
    login(token, done_url, account_number, password, post_url)
    # 获取用户猜你喜欢歌单地址
    url = 'http://www.xiami.com/song/playlist/id/1/type/9'
    r = session.get(url, headers=headers)

    # 2.下载
    q = multiprocessing.JoinableQueue()
    xml_doc = r.content
    sname_iter = re.finditer(r'<songName>(.+?)</songName>', xml_doc)
    sdownload_iter = re.finditer(r'<location>(.+?)</location>', xml_doc)
    # 将要下载的url添加到队列
    for i, j in zip(sname_iter, sdownload_iter):
        q.put([i.group(1), j.group(1)])
    # 使用多进程下载
    for i in xrange(8):
        cons_p = multiprocessing.Process(target=download_song, args=(q,))
        cons_p.daemon = True
        cons_p.start()
    q.join()
    print u'全部下载完成'



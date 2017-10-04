# coding=utf-8
'''
下载虾米猜你喜欢所有歌单(未登入状态)
难点：变量作用域
放到if __name__ == '__main__':变量下面作用域在主进程中（队列除外）
而放在上面的headers在子进程中有拷贝
'''
import requests
import re
import multiprocessing
import urllib2

# 放在这里子进程才能知道
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

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
    '''
    下载歌曲
    '''
    while True:
        item = q.get()
        song_name = item[0].decode('utf-8')
        song_durl = decrypt(item[1])
        r = requests.get(song_durl, headers=headers)
        print u'正在下载'+'%s' % song_name
        try:
            with open('%s.mp3' % song_name, 'wb') as f:
                f.write(r.content)
        # 由于容易引发ioerror，我在这里重点捕获这个异常，同时使用finally语句，在发生异常的情况下也能继续执行
        # 我们在接收错误类型的后面定义一个变量e用于接收具体错误信息, 
        # 然后将e接收的错误信息打印。
        except IOError, e:
            print e
        finally:
            q.task_done()

if __name__ == '__main__':
    url = 'http://www.xiami.com/song/playlist/id/1/type/9'
    q = multiprocessing.JoinableQueue()
    # 1.获取歌曲名称和歌单
    r = requests.get(url, headers = headers)
    xml_doc = r.content
    sname_iter = re.finditer(r'<songName>(.+?)</songName>', xml_doc)
    sdownload_iter = re.finditer(r'<location>(.+?)</location>', xml_doc)
    # 2.建立多进程
    for i in xrange(8):
        cons_p = multiprocessing.Process(target=download_song, args=(q,))
        cons_p.daemon = True
        cons_p.start()
    # 3.建立歌曲队列
    for i, j in zip(sname_iter, sdownload_iter):
        q.put([i.group(1), j.group(1)])
    q.join()
    print u'全部下载完成'



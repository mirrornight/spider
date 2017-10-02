# coding=utf-8
'''
找到虾米猜你喜欢中所有歌曲对应的id号
1.猜你喜欢的歌单页面
http://www.xiami.com/play?ids=/song/playlist/id/1/type/9
首先试用上面这个url，发现下载下来的页面是个播放页面，歌曲的信息应该是异步加载的
http://www.xiami.com/song/play?ids=/song/playlist/id/12372/type/1
http://www.xiami.com/song/playlist/id/12372
发现与单首歌曲的播放地址有点像，因此推断猜你喜欢歌单的xml地址对应如下
http://www.xiami.com/song/playlist/id/1/type/9
查询抓取的xhr，发现一个请求http://www.xiami.com/song/playlist/id/1/type/9/cat/json?_ksTS=1506957187441_389&callback=jsonp390
和之前想的一样
'''

import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

url = 'http://www.xiami.com/song/playlist/id/1/type/9'

r = requests.get(url, headers = headers)
xml_doc = r.content
# <songId>1774490672</songId>
sid_iter = re.finditer(r'<songId>(\d+?)</songId>', xml_doc)
sid_list = []
for m in sid_iter:
    if m:
        sid_list.append(m.group(1))
print len(sid_list)
print sid_list

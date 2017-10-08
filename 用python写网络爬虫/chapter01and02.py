# coding=utf-8
'''
《用python写网络爬虫》
书中一二章的代码
代码写得很好值得学习
'''

import urllib2

def download(url, user_agent='wswp', num_retries=2):
    '''
    user_agent用户代理
    num_retries是重试下载次数，默认为两次
    '''
    print 'Downloading:', url
    headers = {'user_agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, num_retries-1)
    return html


import re
import urlparse

def link_crawler(seed_url, link_regex, delay, max_depth=2, scrape_callback=None):
    '''
    seed_url    :要爬取网站的url
    link_regex  :跟踪链接的正则表达式
    delay       :延迟（秒）
    max_depth   :记录到达页面的最大深度
    scrape_callback: 处理抓取行为
    '''
    crawl_queue = [seed_url]
    seen = {seed_url:0}
    throttle = Throttle(delay)
    sc = scrape_callback()

    while crawl_queue:
        url = crawl_queue.pop()
        throttle.wait(url)
        html = download(url)
        # 回调函数
        # links = []
        if scrape_callback:
            # links.extend(sc(url, html) or [])
            sc(url, html)

        depth = seen[url]
        if depth != max_depth:
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)

def get_links(html):
    webpage_regex = re.compile(r'<a href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


import csv, lxml.html
class ScrapeCallback(object):
    '''
    获取指定页面数据，并将数据保存到csv表格中
    '''
    def __init__(self):
        # python2.x中写入CSV时，CSV文件的创建必须加上'b'参数，即csv.writer(open('test.csv','wb'))，不然会出现隔行的现象。
        # 网上搜到的解释是：python正常写入文件的时候，每行的结束默认添加'n’，
        # 即0x0D，而writerow命令的结束会再增加一个0x0D0A，因此对于windows系统来说，就是两行，而采用’ b'参数，用二进制进行文件写入，系统默认是不添加0x0D的。
        self.writer = csv.writer(open('countries.csv', 'wb'))
        self.fields = ('area', 'population', 'country', 'capital', 'languages')
        self.writer.writerow(self.fields)
    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            print row
            self.writer.writerow(row)

import datetime, time
class Throttle(object):
    '''
    记录了每个域名上次访问的时间，如果当前时间距离上次访问时间小于指定延迟，则执行睡眠操作。
    '''
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}
    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                print sleep_secs
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()


link_crawler('http://example.webscraping.com', '/places/default/(index|view)', 1, 3, ScrapeCallback)





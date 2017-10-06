# coding=utf-8
'''
模拟登入虾米
1.获取登入页面的隐藏信息（用于提交表单信息）
登入页面：https://login.xiami.com/member/login
解析这个页面获取如下三条信息：
<input type="hidden" name="_xiamitoken" value="ba24a0adb67e5c15b5e3d483d493a03d" />
<input type="hidden" value="http%3A%2F%2Fwww.xiami.com%2Fmusic%2Fstyle" name="done">
<input type="hidden" value="" name="verifycode">
_xiamitoken:ba24a0adb67e5c15b5e3d483d493a03d
done:http%3A%2F%2Fwww.xiami.com%2F%2F
verifycode:
2.找到提交表单的页面
https://login.xiami.com/passport/login
需要提交的信息
_xiamitoken:ba24a0adb67e5c15b5e3d483d493a03d
done:http%3A%2F%2Fwww.xiami.com%2F%2F
verifycode:
account:18627274839
pw:123456789h
submit:登 录

测试：头信息中accept、Content-Type、Host对登入不影响
但是在提交表单页面的头信息中Referer头字段类型必须要！
'''
import requests
import re

session = requests.Session()

def get_informations(login_url):
    headers = {
        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #'Host': 'login.xiami.com',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }
    r = session.get(login_url, headers=headers)
    # print r.request.headers
    html_doc = r.content
    token = re.search(r'<input type="hidden" name="_xiamitoken" value="(.+?)" />', html_doc).group(1)
    done_url = re.search(r'<input type="hidden" value="(.+?)" name="done">', html_doc).group(1)
    return token, done_url

def login(token, done_url, account_number, password, post_url):
    headers = {
        #'Host': 'login.xiami.com',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        #'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://login.xiami.com/member/login',
        #'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
    data = {
        '_xiamitoken': token,
        'done': done_url,
        'verifycode': '',
        'account': account_number,
        'pw': password,
        'submit': u'登 录',
    }
    r = session.post(post_url, headers=headers, data=data)
    # print r.request.headers


if __name__ == '__main__':
    # 登入页面  
    login_url = 'https://login.xiami.com/member/login'
    # 真实提交表单页面
    post_url = 'https://login.xiami.com/passport/login'
    # 输入账号和密码
    account_number = raw_input('input your account\n')
    password = raw_input('input your password\n')
    headers = {
        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #'Host': 'www.xiami.com',
        #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }

    token, done_url = get_informations(login_url)
    # print token, done_url
    login(token, done_url, account_number, password, post_url)
    test_url = 'http://www.xiami.com/space/collect-fav/u'
    r = session.get(test_url, headers=headers)
    # print r.request.headers
    with open('xiami.html', 'wb') as f:
        f.write(r.content)


# coding=utf-8
"""
版本七

使用账号密码模拟登入github
1.首先进行抓包分析
使用正确密码时，无法获取表单信息
尝试使用错误密码发现表单信息包括
commit: Sign+in
utf8: %E2%9C%93
authenticity_token:
login:
password:
前两个信息是不变的第三个信息隐藏在https://github.com/login页面代码中
<input name="authenticity_token" type="hidden" value="..." />和value值一样

提交表单信息是在https://github.com/session页面中
"""
import requests
import re

# 全局变量
headers = {
    'Host': 'github.com',
    'Referer': 'https://github.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


def get_authenticity_token(login_url):
    r = session.get(login_url, headers = headers)
    # <input name="authenticity_token" type="hidden" value="" />
    pattern = re.compile(r'<input name="authenticity_token" type="hidden" value="(.*)" />')
    match = pattern.findall(r.content)
    if match:
        authenticity_token = match[0]
        return authenticity_token
    else:
        print "can't match authenticity_token"

def login(session_url, username, password):
    # 创建要提交的表单信息
    data = {
        'commit': 'Sign in',
        'utf8': '%E2%9C%93',
        'authenticity_token': get_authenticity_token(login_url),
        'login': username,
        'password': password
    }

    r = session.post(session_url, data = data, headers = headers)
    with open('session.html', 'wb') as f1:
        f1.write(r.content)

if __name__ == '__main__':
    # 登入页面和提交表单页面
    login_url = 'https://github.com/login'
    session_url = 'https://github.com/session'
    # 输入账号和密码
    username = raw_input('input your name\n')
    password = raw_input('input your password\n')

    session = requests.Session()
    login(session_url, username, password)
    # 会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie，
    # 所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
    # 不能保持请求中的header
    # 检验一下同一个会话中是否保持了相同的cookie
    r = session.get('https://github.com/mirrornight', headers = headers)
    print r.request.headers
    # 将页面下载下来从而查看
    # 如果不是txt文件，建议用wb和rb来读写。通过二进制读写，不会有换行问题。
    with open('github.html', 'wb') as f2:
        f2.write(r.content)






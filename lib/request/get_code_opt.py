import requests
import re
import time
from spider_315.lib.spider.chaojiying import Chaojiying_Client
# shareurl = 'https://www.315jiage.cn/c175.aspx'

def get_code_to_new_html(shareurl):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    response = requests.get(shareurl, headers=headers)
    cookie = response.headers['set-cookie'].split(';')[0]
    ray = response.headers['cf-ray'].split('-')[0]
    html = response.content
    new_url = re.findall('action="(.+?)"',str(html))[0]
    posturl = 'https://www.315jiage.cn{0}'.format(new_url)
    r = re.findall('(?<=value=").+?(?=")', response.text)[0]
    url = 'https://captcha.su.baidu.com/session_cb?pub=377e4907e1a3b419708dbd00df9e8f79'
    headers = {
        'Host': 'captcha.su.baidu.com',
        'Referer': shareurl,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers).text
    session = response.split('"')[-2]
    url = 'https://captcha.su.baidu.com/image?session='+session+'&pub=377e4907e1a3b419708dbd00df9e8f79'
    response = requests.get(url, headers=headers).content
    with open('验证码.jpg', 'wb') as f:
        f.write(response)
    time.sleep(2)
    chaojiying = Chaojiying_Client('xxxx', 'xxxx', 'xxxx')
    im = open('验证码.jpg', 'rb').read()
    yanzhengma = chaojiying.PostPic(im, 1902)['pic_str']
    print('验证码: {}'.format(yanzhengma))
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'referer': shareurl,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    data = {
        'r': r,
        'id': ray,
        'captcha_challenge_field': session,
        'manual_captcha_challenge_field': yanzhengma,
    }
    response = requests.post(posturl, headers=headers, data=data)
    return  response.content
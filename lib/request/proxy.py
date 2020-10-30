
from bs4 import BeautifulSoup
import requests
from lib.request.headers import create_headers

proxys_src = []
proxys = []


def spider_proxyip(num=10):
    try:
        url = 'http://www.xicidaili.com/nt/1'
        req = requests.get(url, headers=create_headers())
        source_code = req.content
        print(source_code)
        soup = BeautifulSoup(source_code, 'lxml')
        ips = soup.findAll('tr')

        for x in range(1, len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            proxy_host = "{0}://".format(tds[5].contents[0]) + tds[1].contents[0] + ":" + tds[2].contents[0]
            proxy_temp = {tds[5].contents[0]: proxy_host}
            proxys_src.append(proxy_temp)
            if x >= num:
                break
    except Exception as e:
        print("spider_proxyip exception:")
        print(e)

def check_ip(ip_info):
    """测试IP地址是否有效"""
    ip_url = ip_info['ip'] + ':' + str(ip_info['port'])
    proxies = {'http': 'http://' + ip_url, 'https': 'https://' + ip_url}
    res = False
    try:
        request = requests.get('http://icanhazip.com/', headers=create_headers(), proxies=proxies, timeout=10)
        if request.status_code == 200:
            res = True
    except Exception as error_info:
        res = False
    return res


if __name__ == '__main__':
    proxy = {
        'ip':'58.220.95.90',
        'port':'9401'
    }
    check_ip(proxy)
    # spider_proxyip(10)
    # print(proxys_src)

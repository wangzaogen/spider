from bs4 import BeautifulSoup
import requests
from lib.request.headers import create_headers
from lib.request.headers import proxy
import re
from lib.item.spu_item import *
from lib.spider.base_spider import *

class SkuSpider(BaseSpider):

    def get_jiage_page_url(self) -> list:
        """
        获取所有产品类型的url
        :return: 返回url list
        """
        type_url_list = []
        home_url = 'https://www.315jiage.cn/default.aspx'
        headers = create_headers()
        response = requests.get(home_url, timeout=10, headers=headers,proxies=proxy)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        type_div = soup.find('div', class_='bd top-sorts')
        type_elements = type_div.find_all('a')
        for types in type_elements:
            if '西药' in str(types.text) or '中成药' in str(types.text) \
                    or '保健食品' in str(types.text) or '医疗器械' in str(types.text) or '消杀用品' in str(types.text):
                continue
            type_url_list.append("https://www.315jiage.cn/{0}".format(types['href']))
        return type_url_list


    def get_tpey_details(self,type_url: str):
        """
        获取每个类型下列表明细
        :param type_url: 类型url
        """
        print("now spide page type_url :{0}".format(type_url))
        headers = create_headers()
        response = requests.get(type_url, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        ## 获取当前类型下的总页数
        total_num = self.get_total_page(soup)
        print('{0}, total num : {1}'.format(type_url, total_num))
        for page_index in range(1, int(total_num)+1):
            if(page_index == 1):
                title_div = soup.find_all('div', class_='title text-oneline')
                for title in title_div:
                    sku_detail_url = title.find('a')['href']
                    self.get_sku_detail_info('https://www.315jiage.cn/{0}'.format(sku_detail_url))
            else:
                headers = create_headers()
                page_sku_url = type_url[0:-5]+'p{0}.aspx'.format(page_index)
                response = requests.get(page_sku_url, timeout=10, headers=headers)
                html = response.content
                soup = BeautifulSoup(html, "lxml")
                title_div = soup.find_all('div', class_='title text-oneline')
                for title in title_div:
                    sku_detail_url = title.find('a')['href']
                    self.get_sku_detail_info('https://www.315jiage.cn/{0}'.format(sku_detail_url))



    def get_sku_detail_info(self, sku_detail_url: str):
        headers = create_headers()
        try:
            response = requests.get(sku_detail_url, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")
            content_div = soup.find('div', id='content')
            p_elements = content_div.find_all('p')[1::]
            spuItem = self.pack_sku_info(p_elements)
            self.pack_sku_instructions(soup)
            print(spuItem.text())
        except Exception as e:
            print('{0},抓取发生异常'.format(sku_detail_url))
            print(headers['User-Agent'])
            print(e)

    def pack_sku_instructions(self, soup: BeautifulSoup):
        instructions_div = soup.find('div',id='tab1')
        li_elements = instructions_div.find_all('li')
        for li in li_elements:
            print(li.text)


    def pack_sku_info(self,p_elements : list) -> SpuItem:
        content_str = ','
        sum_p = len(p_elements)
        specs  = main_diseases = ''
        for index in range(0, sum_p):
            if(1 == index):
                specs = str(p_elements[index].text)
            if(sum_p-1 == index):
                temp_array = str(p_elements[index].text).split('：')
                main_diseases = temp_array[1]
            content_str += str(p_elements[index].text) + ' '

        print(content_str)
        name = re.findall('产品名称：(.+?) ', content_str)[0]
        pinyin = re.findall('拼音简码：(.+?) ', content_str)[0]
        # specs = re.findall('规格：(.+?) ', content_str)[0]
        # dosage = re.findall('剂型：(.+?) ', content_str)[0]
        packing = re.findall('包装单位：(.+?) ', content_str)[0]
        approval_num = re.findall('批准文号：(.+?) ', content_str)[0]
        manufacturer = re.findall('生产厂家：(.+?) ', content_str)[0]
        # main_diseases = re.findall('主治疾病：(.+?) ', content_str)[0]
        spuItem = SpuItem(name, pinyin, specs, '', packing, approval_num, manufacturer, main_diseases)
        return spuItem


    def get_total_page(self, soup: BeautifulSoup) -> int:
        """
        获取 产品类型总页数
        :param soup:
        :return:
        """
        total_span = soup.find('span', class_="p_text p_total")
        total_num = str(total_span.text.strip()).split('/')[1]
        return total_num


if __name__ == '__main__':
    # s = 'https://www.315jiage.cn/c134.aspx'
    # print(s[0:-5]+'p2'+'.aspx')
    skuSpider = SkuSpider('315jiage')
    type_url = skuSpider.get_jiage_page_url()
    skuSpider.get_tpey_details(type_url[0])
    # skuSpider.get_sku_detail_info('https://www.315jiage.cn/x-KeChuan/343599.htm')

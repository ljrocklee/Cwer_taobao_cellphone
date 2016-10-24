import urllib.request
import sys
from bs4 import BeautifulSoup
import re

def get_tb_cellphone():
    s='手机'
    s=urllib.parse.quote(s)
    weburl = 'https://s.taobao.com/list?app=vproduct&vlist=1&q='+s+'&cat=1512&from_type=3c&p4ppushleft=5%2C48&s=0'
    webheader1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    webheader2 = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        #'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.douban.com',
        'DNT': '1'
        }
    print(weburl)
    v_title = '';
    v_price = 0;
    v_src_size = '';
    v_month_sales = 0;
    v_tag1 = '';
    v_tag2 = '';
    webPage=urllib.request.urlopen(weburl)
    data = webPage.read().decode("utf8")
    page_data = str(BeautifulSoup(data,"html.parser"))                       # 通过BF将网页进行转换
    p_all_detail= re.compile(r'(.*)(\"spus\"\:)(.*)(\,\"spucombo\"\:\{\"status\"\:\"hide\"\})(.*)',re.DOTALL)
    m_all_detail = p_all_detail.match(page_data)
    page_data = str(m_all_detail.group(3)).replace('\"','').replace('[','').replace('{','').replace(']','').replace('}','').split(',')

    print("------------------------------------------------")
    for i in range(len(page_data)):
        sub_data = page_data[i].split(':')
        if sub_data[0] == 'title':
            print("--------------------------------------------------------------")
            print(v_title,v_price,v_src_size,v_month_sales,v_tag1,v_tag2)
            v_title = sub_data[len(sub_data)-1]
        elif sub_data[0] == 'price':
            v_price = sub_data[len(sub_data)-1]
        elif sub_data[0] == 'importantKey':
            v_src_size = sub_data[len(sub_data)-1]
        elif sub_data[0] == 'month_sales':
            v_month_sales = sub_data[len(sub_data)-1]
        elif sub_data[0] == 'tag_info':
            v_tag1 = sub_data[len(sub_data)-1]
        elif sub_data[0] == 'tag':
            v_tag2 = sub_data[len(sub_data)-1]



        '''
        for i in len(page_data):
            print(page_data[i])
        print(sys.getdefaultencoding())
        webPage=urllib.request.urlopen(req)
        data = webPage.read()
        print(data)
        print(type(webPage))
        print(webPage.geturl())
        print(webPage.info())
        print(webPage.getcode())
        '''
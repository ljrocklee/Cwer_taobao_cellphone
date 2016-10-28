import urllib.request
from bs4 import BeautifulSoup
import re
import pymysql

def get_tb_cellphone():

    cat_name=urllib.parse.quote('手机')
    weburl = 'https://s.taobao.com/list?app=vproduct&vlist=1&q=%s&cat=1512&from_type=3c&p4ppushleft=5%%2C48&s=%d'
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
    str_sql = 'insert into T_taobao_cellphone(cp_name ,cp_price ,cp_src_size ,cp_month_sales ,cp_tag1 ,cp_tag2)' \
              ' values(%s,%s,%s,%s,%s,%s)'
    conn = pymysql.connect(host = 'localhost', db = '--', user = '--', password = '--',charset = 'utf8')
    try:

        tb_cur = conn.cursor();
        webPage_total=urllib.request.urlopen(weburl%(cat_name,0))
        total_message = webPage_total.read().decode("utf8")
        page_message = str(BeautifulSoup(total_message,"html.parser"))                       # 通过BF将网页进行转换
        r_page_message = re.compile(r'(.*)(\"pager\"\:\{\"status\"\:\"show\"\,\"data\"\:\{)(.*)(\"spus\"\:)',re.DOTALL)
        m_all_detail = r_page_message.match(page_message)
        page_message = str(m_all_detail.group(3)).replace('\"','').replace('[','').replace('{','').replace(']','').replace('}','').split(',')
        page_size = int(page_message[0].split(':')[1])
        totalPage = int(page_message[1].split(':')[1])
        currentPage = 1
        totalCount = page_message[3].split(':')[1]
        print(totalPage)
        while currentPage <= totalPage:
            tb_cur = conn.cursor();
            v_title = '';
            v_price = 0;
            v_src_size = '';
            v_month_sales = 0;
            v_tag1 = '';
            v_tag2 = '';
            page_valueset = [];
            webPage=urllib.request.urlopen(weburl%(cat_name,(currentPage-1)*page_size))
            print(weburl%(cat_name,(currentPage-1)*page_size))
            data = webPage.read().decode("utf8")
            page_data = str(BeautifulSoup(data,"html.parser"))                       # 通过BF将网页进行转换
            p_all_detail= re.compile(r'(.*)(\"spus\"\:)(.*)(\,\"spucombo\"\:\{\"status\"\:\"hide\"\})(.*)',re.DOTALL)
            m_all_detail = p_all_detail.match(page_data)
            page_data = str(m_all_detail.group(3)).replace('\"','').replace('[','').replace('{','').replace(']','').replace('}','').replace('\\','').split(',')
            print(page_size, totalPage ,currentPage,totalCount)
            #while currentPage < int(totalPage):
            for i in range(len(page_data)):
                sub_data = page_data[i].split(':')
                print(sub_data)
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
                    page_valueset.append((v_title,v_price,v_src_size,v_month_sales,v_tag1,v_tag2))
            print(page_valueset)
            tb_cur.executemany(str_sql,page_valueset)
            conn.commit()
            tb_cur.close()
            currentPage += 1
    except Exception as e:
        print(e)
    finally:
        conn.close()




get_tb_cellphone()


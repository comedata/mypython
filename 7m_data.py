import time
import requests
import chardet
from bson import json_util as jsonb
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient


qm_url = 'https://www.qimai.cn/account/signin'
qm_top_app_url = 'https://www.qimai.cn/rank/index/brand/free/country/cn/genre/6014/device/iphone'
qcc_url='https://www.tianyancha.com/search?key='


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Referer':'http://www.qichacha.com/search?key=360',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest'

}


def __init__():
    # 初始化配置根据自己chromedriver位置做相应的修改
    # chromedriver = r"D:\chromedriver\chromedriver.exe"
    # os.environ["webdriver.chrome.driver"] = chromedriver

    brower = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe")
    return brower

def request(url):
    try:
        print(url)
        response = requests.get(url,headers=headers,timeout=30)
        if response.status_code==200:
            return response
        return None
    except requests.RequestException:
        for x in range(2):
            response = requests.get(url, headers=headers, timeout=30)
            return response


def login(url):

    browser = __init__()
    browser.get(url)
    user = browser.find_element_by_name('username')
    # 输入账号
    user.send_keys('17611549970')
    pws = browser.find_element_by_name('password')
    # 输入密码
    pws.send_keys('qm571754723')
    enter = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/form/div[4]/div/button')
    # 回车登录
    enter.send_keys(Keys.ENTER)
    time.sleep(2)

    browser.get(qm_top_app_url)
    time.sleep(5)
    data = browser.find_element_by_xpath('//*[@id="rank-top-list"]/div[1]/div[2]/div[1]/div[4]/div[2]/ul/li[2]/a')
    data.click()
    time.sleep(3)

    #下拉刷新并解析
    for x in range(18):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        if x > 3:
            html=soup_html(browser.page_source)
            soup_company(html)
            time.sleep(3)
    time.sleep(10)
    browser.close()

def soup_html(html):
    return BeautifulSoup(html, 'lxml')

def soup_company(soup):
        for tr in soup.select('tr'):
            index=tr.select('.index')

            if len(index)>0:
                inds = index[0].text

                icon_list = tr.select('td')
                company = icon_list[7].text

                for td in tr.select('td'):
                    for c in td.select('.dark-green'):
                            company = c.text
                    for c in td.select('.name'):
                        game_app = c.text.strip().lstrip().rstrip(',')
            else:
                inds=''
                company=''
                game_app=''

            product = {
                'indexs': inds,
                'game_app': game_app,
                'company': company,
            }
            print(product)

            mymongo(product)

def mymongo(maps):
    client=MongoClient('localhost',27017)
    db=client.qimai
    collection = db.product
    collection.insert(maps)

company = []
def query_db():
    client=MongoClient('localhost',27017)
    db = client.qimai
    collection = db.product

    db_index=collection.distinct('game_app')
    db_company=db_index[1:]
    print(db_company)

    for x in db_company:
        index = jsonb.dumps(list(collection.find({'indexs': x})))
        chardet.detect(index)
        print(index.encode('utf-8'))
        sum=collection.find({'indexs': x}).count()
        for i in range(1,sum):
            #print(i)
            collection.remove({'indexs':x},0)

#企查查搜索匹配对应公司名称
def search():
    for x in company[1:]:
        print(x)
        x.strip().lstrip().rstrip(',')
        print(x)
        respanse=request(qcc_url+'360')

        print(soup_html(respanse))
        break


if __name__ == '__main__':
   login(qm_url)

# for fid in collection_bbs.distinct('fid'):
#     for tid in collection_bbs.find({'fid': fid}).distinct('tid'):
#         num = collection_bbs.find({'fid': fid, "tid": tid}).count()
#         for i in range(1, num):
#             collection_bbs.remove({'fid': fid, "tid": tid}, 0)


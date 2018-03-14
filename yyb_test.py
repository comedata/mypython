import requests
import json
import jsonpath
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient


# url='http://sj.qq.com/myapp/category.htm'

headers={
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'0',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest'
}

def request(url):
    try:
        response = requests.get(url,headers=headers,timeout=30)
        if response.status_code==200:
            return response
        return None
    except requests.RequestException:
        for x in range(2):
            response = requests.get(url, headers=headers, timeout=30)
            return response

def sou_html(url):
    print(url)
    html=request(url)
    html=BeautifulSoup(html.text,'lxml')
    return html

#
# menu_list=[]
# def menu_game(url):
#     menu=sou_html(url+'?orgame=2')
#     all_game_list=menu.select('.menu-junior')
#     for x in all_game_list:
#         for i in x.select('li'):
#             #print(i)
#             a=i.find('a')
#             if a==None:
#                 print('a=null')
#             else:
#                 menu_list.append(a.get('href'))
#     get_all_page()
#
# game_projects=[]
# def get_game_projects():
#     for x in menu_list:
#         all_game = sou_html(url+x)
#         for i in all_game.select('.app-info-desc'):
#             game_projects.append(i.select('a')[0].get('href'))
#     print(len(game_projects))
#
pages=[147,121,149,144,151,148,153,146]

def get_all_page():
        for x in range(200):
            html=sou_html('http://sj.qq.com/myapp/cate/appList.htm?orgame=2&categoryId='+'146'+'&pageSize=20&pageContext='+str(x))
            for x in html.select('p'):
                game_json=x.text
                print(game_json)
                unicodestr=json.loads(game_json)
                company_list=jsonpath.jsonpath(unicodestr,'$..authorName')
                print(company_list)
                if len(company_list)>0:
                    for x in company_list:
                        print(x)
                        mymongo({'copmpany': x})
                else:
                    break


def query():
    client=MongoClient('localhost',27017)
    db=client.yyb
    collection=db.product
    company=collection.find().distinct('copmpany')
    for x in company:
        print(x)


def mymongo(maps):
    client=MongoClient('localhost',27017)
    db=client.yyb
    collection = db.product
    collection.insert(maps)

#{"total":1,"count":0,"obj":[],"pageContext":"","success":true,"pageSize":null,"msg":"success"}
#{"total":1,"count":20,"obj"
if __name__ == '__main__':
    #get_all_page()
    query()



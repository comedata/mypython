import requests

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from pymongo import MongoClient


sid_url='http://zhushou.360.cn/list/index/cid/2?page='
company_url='http://zhushou.360.cn/detail/index/soft_id/'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
}

page=[]
sid1=[]

def request(url):
    try:
        html = requests.get(url,headers=headers,timeout=30)
        if html.status_code==200:
            return html
        return None
    except RequestException:
        return requests.get(url,headers=headers,timeout=30)


def soup_html(url):
    sid_html=request(url)
    sid_html.status_code='utf-8'
    soup = BeautifulSoup(sid_html.text, 'lxml')
    return soup

def soup_html_sid(url):
    soup=soup_html(url)
    for h3 in soup.select('#iconList'):
        #print(h3.select('h3'))
        for sid in h3.select('h3'):
            #print(sid.select('a'))
            for sid in sid.select('a'):
               # print(sid['sid'])
                sid1.append(sid['sid'])


def soup_html_company(i):
    #print(soup_html(company_url+sid1[i]))
    #解析公司名称
    data = soup_html(company_url + sid1[i])
    for soup in data.select('table'):
        gs=soup.select('td')[0].text
        save_text(gs[3:])
        print(gs[3:])
    map={'company':gs[3:]}
    mongobd(map)

def save_text(content):
    with open('360zhushou.txt','a') as f:
        f.write(content+'\n')
        f.close()

def mongobd(maps):
    client=MongoClient('localhost',27017)
    db=client.mymong
    map=db.company
    map.insert(maps)

def get_page_url():
    for x in range(1, 51):
        page.append(sid_url+str(x))

def main():
    #获取出所有page的url
    if len(page)==0:
        get_page_url()
    fun()

def fun():
    for x in page:
        # 开始解析单页游戏公司所有sid
        soup_html_sid(x)
        #print(' url  :  ' + x)
        for i in range(len(sid1)):
            # 根据sid再去解析所有公司名称
            soup_html_company(i)

        del sid1[:]

def query():
    client=MongoClient('localhost',27017)
    db=client.yyb
    collection=db.product
    company=collection.find().distinct('copmpany')
    for x in company:
        print(x)

if __name__ == '__main__':
     main()






import time
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

url='https://www.qimai.cn/account/signin'
app_url='https://www.qimai.cn/rank/index/brand/free/country/cn/genre/6014/device/iphone'

company=[]

def __init__():
    # 初始化配置根据自己chromedriver位置做相应的修改
    #chromedriver = r"D:\chromedriver\chromedriver.exe"
    # os.environ["webdriver.chrome.driver"] = chromedriver

    brower = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe")
    return brower

def login(url):
    browser=__init__()
    browser.get(url)
    user=browser.find_element_by_name('username')
    #输入账号
    user.send_keys('17611549970')
    pws=browser.find_element_by_name('password')
    #输入密码
    pws.send_keys('qm571754723')
    enter=browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/form/div[4]/div/button')
    #回车登录
    enter.send_keys(Keys.ENTER)
    time.sleep(5)
    # #鼠标悬浮在app榜单上
    # action=browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/ul/li[2]/div/div[1]/div')
    # # app_top = browser.find_element_by_xpath('')
    # ActionChains(browser).move_to_element(action).perform()
    browser.get(app_url)

    #
    time.sleep(8)

    for x in range(18):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(5)
        if x%3:

            get_html(browser.page_source)

    time.sleep(10)
    print(len(company))
    browser.close()

def soup_html(html):
    return BeautifulSoup(html, 'lxml')

def get_html(html):
    doc=pq(html)
   
    product={
        'game':doc('.data-table .app-info-wrap .app-info .name').text(),
        'writer':doc('.data-table .app-info-wrap .app-info .company').text(),
        'company':doc('.data-table .dark-green').text()
    }
    print(product)





def save_text(text):
    with open('七麦.txt','a') as f:
        f.write(text+'\n')
        f.close()

if __name__ == '__main__':
    __init__()
    login(url)



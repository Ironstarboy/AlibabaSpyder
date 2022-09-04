import requests
from selenium import webdriver
from time import sleep
import pandas as pd
import os
import numpy as np
import random
import threading
import myio
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# TODO ip代理，ip池


class Spyder:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.128 Safari/537.36 ',
            'Host': 'wenshu.court.gov.cn',
            # 'Origin': 'https://wenshu.court.gov.cn',
            'sec-ch-ua': 'Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99',
            # 'Referer': 'https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=27cc21'
            #            '6a1f2f1f52fb1f145752d59ee2&s21=%E7%BB%8F%E6%B5%8E%E7%8A%AF%E7%BD%AA',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '',
            'page_load_strategy':'none'
        }

        self.url = 'https://www.alibaba.com/'
        self.request = requests.session()
        # 加载需要执行的js文件
        # self.ctx = node.compile(open('cipher.js', encoding='utf-8').read())
        chrome_options = webdriver.ChromeOptions()
        # 让浏览器不显示自动化测试
        chrome_options.add_argument('disable-infobars')
        # 禁止加载图片
        # prefs = {'profile.managed_default_content_settings.images': 2}
        # chrome_options.add_experimental_option('prefs', prefs)
        self.chrome = webdriver.Chrome( options=chrome_options)

        self.chrome.set_page_load_timeout(6)

    def getPrice(self,goodsInfo:pd.DataFrame):
        url = goodsInfo['url']
        productName = goodsInfo['productName']
        smallAmountXpath = goodsInfo['smallAmountXpath']
        largeAmountXpath = goodsInfo['largeAmountXpath']
        samllPriceXpath = goodsInfo['samllPriceXpath']
        largePriceXpath = goodsInfo['largePriceXpath']
        self.chrome.set_page_load_timeout(3)
        try:
            # TODO 打开新标签页再操作，还是原本的标签页操作呢
            self.chrome.get(url)
            sleep(1)
        except Exception as e:
            print('元素实际已加载出，跳过加载')
        smallAmount=self.chrome.find_element_by_xpath(smallAmountXpath).text
        largeAmount=self.chrome.find_element_by_xpath(largeAmountXpath).text
        lowPrice=self.chrome.find_element_by_xpath(samllPriceXpath).text
        highPrice=self.chrome.find_element_by_xpath(largePriceXpath).text

        sleep(1)
        save2xlsx(productName,smallAmount,largeAmount,lowPrice,highPrice)

    def saveUrlFromSearch(self,productName):
        try:
            self.chrome.get(f'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&tab=all&SearchText={productName}')
        except Exception as e:
            print('元素实际已加载出，跳过加载')
        finally:
            print('加载完毕')

        # 如果结果不是化肥，就搜不出来

        try:
            fisrtOutcome = self.chrome.find_element_by_xpath(
                '//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/h2/a/p')
            fisrtOutcome.click()
        except Exception:
            print('不是化肥')
            self.chrome.quit()
            return '',''

        # 切换标签页
        handles = self.chrome.window_handles
        self.chrome.switch_to.window(handles[-1])

        try:
            self.chrome.title # 先加载一次让页面超时，停止加载
        except Exception:
            ...
        title:str =self.chrome.title
        title=title[:title.index('-')]
        print(title)

        url=self.chrome.current_url
        print(url)
        self.chrome.quit()
        return title,url

def getGoodsInfo():
    df=pd.read_csv('productDetail.csv')
    return df

def save2xlsx(productName,smallAmount,largeAmount,lowPrice,highPrice):
    outFileName='alibaba商品爬取结果.csv'
    spyderTime=pd.datetime.now()
    if not os.path.exists(outFileName):
        with open(outFileName,'w',encoding='utf8') as f:
            f.write('产品名,采购范围1,产品价格1,采购范围2,产品价格2,爬取时间\n')
    else:
        with open(outFileName, 'a') as f:
            f.write(f'{productName},{smallAmount},{lowPrice},{largeAmount},{highPrice},{spyderTime}\n')

# TODO 写一个搜索结果筛选网页。记录筛选url


if __name__ == '__main__':
    spyder=Spyder()
    # goodsInfo:pd.DataFrame=getGoodsInfo()
    # for index, goodsInfo in goodsInfo.iterrows():
    #     haveNan=0
    #     for i in goodsInfo:
    #         if pd.isna(i):
    #             haveNan=1
    #             print(f"{goodsInfo['productName']} 暂未在alibaba搜寻到")
    #             break
    #     if not haveNan:
    #         spyder.getPrice(goodsInfo)
    # print('价格更新完成')

    spyder.saveUrlFromSearch()





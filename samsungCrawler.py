from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
from selenium import webdriver
import chromedriver_autoinstaller
import time
import re
import requests

chromedriver_autoinstaller.install()
wd = webdriver.Chrome()

def finance(result):
    for page in range(1,666):
        samsung_url = 'https://finance.naver.com/item/sise_day.naver?code=005930&page=%d' %page
        req = requests.get(samsung_url, headers={'User-agent': 'Mozilla/5.0'})
        soupSamsung = BeautifulSoup(req.text, 'html.parser')

        tr_tag = soupSamsung.find_all("tr", {"onmouseover":"mouseOver(this)"})
        for tr in tr_tag:
            try:
                day = tr.find("span", {"class":"tah p10 gray03"}).string
                temp1 = tr.find("span", {"class":"tah p11 red02"})
                temp2 = tr.find("span", {"class":"tah p11 nv01"})
                if temp1 is not None and temp2 is None:
                    temp1 = temp1.string
                    temp1 = re.sub("\W+","",temp1)
                    fluctuation = 0
                    fluctuation += int(temp1)
                elif temp1 is None and temp2 is not None:
                    temp2 = temp2.string
                    temp2 = re.sub("\W+","",temp2)
                    fluctuation = 0
                    fluctuation -= int(temp2)
                elif temp1 is None and temp2 is None:
                    fluctuation = 0
                result.append([day]+[fluctuation])
            except:
                continue
        print("%d페이지 완료" %page)

def saumsung(result):
    for page in range(0,100):
        query = '%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&oq=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90'
        samsung_url = "https://patents.google.com/?assignee=" + query + '&page=%d' %page
        wd.get(samsung_url)
        time.sleep(1)
        html = wd.page_source
        soupSamsung = BeautifulSoup(html, "html.parser")
    
        h4_tag = soupSamsung.find_all("h4", attrs={"class":"dates style-scope search-result-item"})
    
        for item in h4_tag:
            try:
                day = re.search('Granted (.+?) Published', str(item)).group(1)
                day_clear = re.sub("\W+", "", day)
                result.append(day_clear)
            except:
                continue
        print("%d페이지 완료" %page)
    return result

def main():
    result = []
    print("Samsung crawling >>>>>>>>>>>>>>>>>>>>>>>>>>")
    saumsung(result) #[CODE 1] 호출
    saumsung_tbl = pd.DataFrame(result, columns = ["특허 등록일"])
    saumsung_tbl.to_csv("./samsung.csv", encoding = "utf-8", mode = "w", index = True)
    del result[:]
    print("finance crawling >>>>>>>>>>>>>>>>>>>>>>>>>>")
    finance(result)
    finance_tbl = pd.DataFrame(result, columns=["Date", "fluctuation"])
    finance_tbl.to_csv("./samsung_finance.csv",  encoding = "utf-8", mode = "w", index = True)
    del result[:]

if __name__ == '__main__':
    main()
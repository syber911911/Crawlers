from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

result = []
def finance(result):
    for page in range(1,39):
        Kospi_url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page=%d' %page
        print(Kospi_url)
        html = urllib.request.urlopen(Kospi_url)
        soupKospi = BeautifulSoup(html, 'html.parser')
        tag_tbody = soupKospi.find('tbody')
        for stock in tag_tbody.find_all('tr'):
            if len(stock) <= 2:
                continue
            stock_td = stock.find_all('td')
            stock_span = stock.find_all('span')
            stock_name = stock_td[1].string
            stock_now = stock_td[2].string
            stock_change = stock_span[0].string.strip()
            stock_ud = stock_span[1].string.strip()
            stock_face = stock_td[5].string
            stock_cap = stock_td[6].string
            stock_number = stock_td[7].string
            stock_foreigner = stock_td[8].string
            stock_trade = stock_td[9].string
            stock_per = stock_td[10].string
            stock_roe = stock_td[11].string
            result.append([stock_name]+[stock_now]+[stock_change]+[stock_ud]+[stock_face]+[stock_cap]+[stock_number]+[stock_foreigner]+[stock_trade]+[stock_per]+[stock_roe])
    return

def main():
    result = []
    print(">>>>>>>Naver Finance Crawler<<<<<<<")
    finance(result) 
    stock_tbl = pd.DataFrame(result, columns = ('종목명', '현재가', '전일비', '등락율', '액면가', '시가총액', '상장주식수', '외국인비율', '거래량', 'PER', 'ROE'))
    stock_tbl.to_csv("/Users/hjun/DataScience Example/stock.csv", encoding = "utf-8", mode = "w", index = True)
    del result[:]

if __name__ == '__main__':
    main()  
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import re

def movie1(result):
    for page in range(1,100):
        movie_url = 'https://movie.naver.com/movie/bi/mi/review.naver?code=161242&page=%d' %page
        html = urllib.request.urlopen(movie_url)
        soupMovie = BeautifulSoup(html, 'html.parser')
    
        ul_tag = soupMovie.find('ul', class_='rvw_list_area')
        li_tag = ul_tag.find_all('li')
    
        for li in li_tag:
            a_tag = li.find('a')
            temp = re.search('<a href(.+?)>', str(a_tag)).group(1)
            number = re.sub(r'[^0-9]', '', temp)
            title = li.a.string
            #text = li.p.string
            review_url = 'https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={0}&code=161242&order=#tab'.format(int(number))
            html1 = urllib.request.urlopen(review_url)
            soupReview = BeautifulSoup(html1, 'html.parser')
            div_tag = soupReview.find('div', class_='user_tx_area')
            text = div_tag.get_text()
            result.append([number]+[title]+[text])
    return

def movie2(result):
    for page in range(1,100):
        movie_url = 'https://movie.naver.com/movie/bi/mi/review.naver?code=192608&page=%d' %page
        html = urllib.request.urlopen(movie_url)
        soupMovie = BeautifulSoup(html, 'html.parser')
    
        ul_tag = soupMovie.find('ul', class_='rvw_list_area')
        li_tag = ul_tag.find_all('li')
    
        for li in li_tag:
            a_tag = li.find('a')
            temp = re.search('<a href(.+?)>', str(a_tag)).group(1)
            number = re.sub(r'[^0-9]', '', temp)
            title = li.a.string
            #text = li.p.string
            review_url = 'https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={0}&code=192608&order=#tab'.format(int(number))
            html1 = urllib.request.urlopen(review_url)
            soupReview = BeautifulSoup(html1, 'html.parser')
            div_tag = soupReview.find('div', class_='user_tx_area')
            text = div_tag.get_text()
            result.append([number]+[title]+[text])
    return

def main():
    result = []
    print(">>>>>>>>>Naver Movie Crawler<<<<<<<<<<")
    movie1(result)
    movie1_tbl = pd.DataFrame(result, columns = ('고유번호', '제목', '내용'))
    movie1_tbl.to_csv("./movie/movie1.csv", encoding = "utf-8", mode = "w", index = True)
    del result[:]
    movie2(result)
    movie2_tbl = pd.DataFrame(result, columns = ('고유번호', '제목', '내용'))
    movie2_tbl.to_csv("./movie/movie2.csv", encoding = "utf-8", mode = "w", index = True)
    del result[:]
    
if __name__ == '__main__':
    main() 
import os
import sys
import urllib.request
import datetime
import time
import json
client_id = "YGVmGIseExAF5WhkoHwq"
client_secret = "79PjdX0fAg"

#[CODE 1]
def getRequestUrl(url): #입력받은 url 접속과 검색 요청
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8') #응답 객체를 바이트 배열로 읽어들임.
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" %(urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url) #[CODE 1]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode) #요청 결과를 json 응답으로 받기.
        
#[CODE 3]
def getPostData(post, jsonResult, cnt): #응답 데이터를 정리하여 리스트에 저장.
    title = post["title"] # 검색 결과 문서의 제목
    description = post["description"] #검색 결과 문서 내용 요약
    org_link = post["originallink"] # 검색 결과 문서를 제공하는 언론사의 link
    link = post["link"] # 검색 결과 문서를 제공하는 네이버의 link
    
    #pubDate -> 검색 결과 문서가 네이버에 제공된 시간
    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt':cnt, 'title':title, 'description': description,
                            'org_link':org_link, 'link': org_link, 'pDate':pDate})
    return

#[CODE 0]
def main():
    node = 'news' #크롤링할 대상
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []
    jsonResponse = getNaverSearch(node, srcText, 1, 100) #[CODE 2]
    total = jsonResponse['total'] #총 검색 건수.
    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']: #검색 결과로 title, originallink, link, desciption, pubDate를 제공.
            cnt += 1
            getPostData(post, jsonResult, cnt) #[CODE 3]

        start = jsonResponse['start'] + jsonResponse['display'] # -> start -> 101, 201, 301, .... 1001까지 변화.
        #[start] 필드의 출력은 검색 결과 문서 중 문서의 시작점, [display] 필드의 출력은 검색된 결과 총수.
        jsonResponse = getNaverSearch(node, srcText, start, 100) #[CODE 2]
        #요청 변수 start는 검색 시작 위치 1(기본값)-1000(최대값), display는 검색 결과 출력 건수 10(기본값)-100(최대값)
    print('전체 검색 : %d 건' %total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True,
                                     ensure_ascii = False)

        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" %(cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))

if __name__ == '__main__':
    main()


 
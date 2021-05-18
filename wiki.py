# 抓取ptt八卦版的網頁原始碼(html)
import urllib.request as req
import bs4
import json
import collections
import re
#建立一個Request物件，附加request haders 的資訊
#模擬request

def crawl(url):

    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    })
    #攔截response
    #透過urlpopen開啟網頁
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    """
    with ... as ...
    response=req.urlopen(request)#連接成功後回傳的
    data=response.read().decode("utf-8")#將回傳的內容解碼
    結束、處理例外
    """

    #解析原始碼
    root=bs4.BeautifulSoup(data,"html.parser")
    #這裡的root就是解析完成後，所產生的結構樹物件，接下來所有資料的搜尋、萃取等操作都會透過這個物件來進行。
    #html.parser 為python內建的解析器，lxml為解析速度最快的

    content=root.find("div",class_="mw-parser-output")#尋找所有class="
    awords=content.find_all("a");
    s=set()
    for aword in awords:
        if aword.string!= None:#如果標題包含 a標籤(沒有被刪除)
            z= re.match('^\[',aword.string);
            #if z:
                #print("!!!!!!!!!!!!!!!!!!!"+aword.string)
            if not(z):
                print(aword.string)
                str(aword.string)
                s.add(aword.string)
                with open('wikicrawler.txt', 'a', encoding='utf-8') as f:#用utf-8解碼中文

                    print(aword.string,file=f)
    print("int set____________________________________________________________-")
    for item in s:
        print(item)
def intopage(url):
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    })
    #攔截response
    #透過urlpopen開啟網頁
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    """
    with ... as ...
    response=req.urlopen(request)#連接成功後回傳的
    data=response.read().decode("utf-8")#將回傳的內容解碼
    結束、處理例外
    """

    #解析原始碼
    root=bs4.BeautifulSoup(data,"html.parser")
    #這裡的root就是解析完成後，所產生的結構樹物件，接下來所有資料的搜尋、萃取等操作都會透過這個物件來進行。
    #html.parser 為python內建的解析器，lxml為解析速度最快的
    title = root.find("h1").string
    match=re.match("^分類",title)
    if match:
        link_block = root.find("td",style_="vertical-align: top; padding-bottom: 1em")#尋找所有class="
        links=link_block.find_all("a");
        for link in links :
            intopage(link[href])
    else:
        crawl(url);
url="https://zh.wikipedia.org/wiki/%E5%A4%A9%E7%87%95%E5%BA%A7"
#f = open('wikicrawler.txt', 'w')
#a=5
#print(a,file=f)
crawl(url)
#f.close()

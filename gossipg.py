# 抓取ptt八卦版的網頁原始碼(html)
import urllib.request as req
url="https://www.ptt.cc/bbs/Gossiping/index.html"
#建立一個Request物件，附加request haders 的資訊
#模擬request
request=req.Request(url, headers={
    "cookie":"over18=1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
})


#攔截response
#透過urlpopen開啟網頁
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
"""
response=req.urlopen(request)#連接成功後回傳的
data=response.read().decode("utf-8")#將回傳的內容解碼
結束、處理例外
"""

#print(data)
#解析原始碼，取得每篇文章的標題
import bs4
root=bs4.BeautifulSoup(data,"html.parser")
#這裡的root就是解析完成後，所產生的結構樹物件，接下來所有資料的搜尋、萃取等操作都會透過這個物件來進行。
#html.parser 為python內建的解析器，lxml為解析速度最快的

#print(root.title.string)
titles=root.find_all("div",class_="title")#尋找所有class="title"的div標籤
for title in titles:
    if title.a != None:#如果標題包含 a標籤(沒有被刪除). 印出來
        print(title.a.string)
f = open('gossipingcrawler_test.txt', 'w')
f.write(root.title.string)
f.write("\n")
for title in titles:
    if title.a != None:
        f.write(title.a.string)
        f.write("\n")
f.close()

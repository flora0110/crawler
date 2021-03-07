# 抓取ptt八卦版的網頁原始碼(html)
import urllib.request as req
import bs4
import json
import collections

#二維dict
def addtwodimdict(thedict, key_a, key_b, val):
    #檢查key_a是否存在
    if key_a in thedict:
        #update()把字典的键值對更新到dict
        thedict[key_a].update({key_b: val})
        #thedict = {key_a:{key_b:val}}
    else:
        thedict.update({key_a:{key_b: val}})
        #thedict{key_a} = {}
        #thedict = {key_a:{key_b:val}}


#進入某頁並回傳下頁url
def crawl(url):
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
    with ... as ...
    response=req.urlopen(request)#連接成功後回傳的
    data=response.read().decode("utf-8")#將回傳的內容解碼
    結束、處理例外
    """

    #解析原始碼
    root=bs4.BeautifulSoup(data,"html.parser")
    #這裡的root就是解析完成後，所產生的結構樹物件，接下來所有資料的搜尋、萃取等操作都會透過這個物件來進行。
    #html.parser 為python內建的解析器，lxml為解析速度最快的

    titles=root.find_all("div",class_="title")#尋找所有class="title"的div標籤
    for title in titles:
        if title.a != None:#如果標題包含 a標籤(沒有被刪除)
            #print(title.a.string)
            #print(title.a["href"])
            link=title.a["href"]
            crawl_text(link)#進入此文章

    #找到下頁的bottom
    nextpage = root.find("a",string = "‹ 上頁")
    return nextpage["href"]#回傳bottom's url

#爬文章內容
def crawl_text(url):
    url = "http://www.ptt.cc"+ url
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    root=bs4.BeautifulSoup(data,"html.parser")

    #標題
    header = root.find_all('span','article-meta-value')

    author = header[0].text
    board = header[1].text
    title = header[2].text
    time = header[3].text

    #抓出內容
    main_container=root.find("div",id="main-content")
    #把文字抓出來
    all_text = main_container.text
    #把內容透過"※"切割成兩個陣列，pre_text為第一個
    #內文的底是※
    pre_text = all_text.split('※')
    pre_text = all_text.split('※')[0]
    #把文字用'\n'切開
    texts=pre_text.split('\n')
    #拿掉第一行:標題
    contents = texts[1:]
    #將元素用指定字符連接成新字串
    content = '\n'.join(contents)

    #打開file(f)
    with open('gossip_crawl.json', 'a', encoding='utf-8') as f:#用utf-8解碼中文
        #com_dict = collections.OrderedDict()#回應dict
        com_dicts = collections.defaultdict()
        pushs=root.find_all("div",class_="push")#抓取推文
        n=1#推文數
        for push in pushs:

            tag = push.find("span", {'class': 'push-tag'}).text
            user = push.find("span",class_="f3 hl push-userid")
            com = push.find("span",class_="f3 push-content")
            com_time=push.find("span",class_="push-ipdatetime")

            #圖片要印網址
            if com.a != None:
                com=com.a["href"]
            else:
                #print(com.string)
                com=com.string

            str(n)#int to string
            #把推文資料存進com_dict

            com_dict = collections.defaultdict()
            """
            addtwodimdict(com_dict,n,"user", user.string)
            addtwodimdict(com_dict,n,"tag", tag)
            addtwodimdict(com_dict,n,"com", com)
            """
            #com_dict = collections.defaultdict
            com_dict['tag']=(tag)
            com_dict['user']=(user.string)
            com_dict['com']=(com)
            com_dict['time']=(com_time.string)
            #print(com_dict)
            com_dicts[n]=com_dict
            int(n)#string to int
            n=n+1

        dic = collections.OrderedDict()
        dic['title']=title
        dic['time']=time
        dic['author']=author
        dic['content']=content
        dic['comment']=com_dicts
        d=dict(dic)
        #d=[{"author":author,"board":board,"title":title,"time":time,"content":content,"comment":com_dict}]
        json.dump(d,f,ensure_ascii=False,sort_keys=False, indent=4);
        """
        sort_keys : 這個應該字面上很好理解了，是否排序Key。
        indent : 若給非負整數，會幫你格式編排好看依照（填入的）數字等級。
        """
        print("writing...")
url="https://www.ptt.cc/bbs/Gossiping/index.html"
f = open('gossipingcrawler_test.txt', 'w')
n=0
while n<2:
    url = "http://www.ptt.cc"+ crawl(url)
    n+=1
f.close()

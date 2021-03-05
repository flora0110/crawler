# 抓取ptt八卦版的網頁原始碼(html)
import urllib.request as req
import bs4

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
    response=req.urlopen(request)#連接成功後回傳的
    data=response.read().decode("utf-8")#將回傳的內容解碼
    結束、處理例外
    """
    #print(data)

    #解析原始碼
    root=bs4.BeautifulSoup(data,"html.parser")
    #這裡的root就是解析完成後，所產生的結構樹物件，接下來所有資料的搜尋、萃取等操作都會透過這個物件來進行。
    #html.parser 為python內建的解析器，lxml為解析速度最快的

    #print(root.title.string)
    titles=root.find_all("div",class_="title")#尋找所有class="title"的div標籤
    for title in titles:
        if title.a != None:#如果標題包含 a標籤(沒有被刪除). 印出來
            print(title.a.string)
            print(title.a["href"])
            link=title.a["href"]
            crawl_text(link)

    """
    f.write(root.title.string)
    f.write("\n")
    for title in titles:
        if title.a != None:
            f.write(title.a.string)
            f.write("\n")
    """

    nextpage = root.find("a",string = "‹ 上頁")
    return nextpage["href"]

def crawl_text(url):
    url = "http://www.ptt.cc"+ url
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    root=bs4.BeautifulSoup(data,"html.parser")
    #print(data)

    header = root.find_all('span','article-meta-value')

    author = header[0].text
    print("author:")
    print(author)
    board = header[1].text
    print("board:")
    print(board)
    title = header[2].text
    print("title:")
    print(title)
    time = header[3].text
    print("time:")
    print(time)

    #抓出內容
    main_container=root.find("div",id="main-content")
    #把文字抓出來
    all_text = main_container.text
    #把內容透過"--"切割成兩個陣列，pre_text為第一個
    #內文的底是--
    pre_text = all_text.split('※')
    pre_text = all_text.split('※')[0]
    """
    post_text = all_text.split('※')[2]
    print("_________________pre:")
    print(pre_text)
    print("_________________post:")
    print(post_text)
    print("______________________")
    """
    #把文字用'\n'切開
    texts=pre_text.split('\n')
    """
    com_texts = post_text.split('\n')
    """
    #拿掉第一行:標題
    contents = texts[1:]
    #comments = com_texts[3:]
    #將元素用指定字符連接成新字串
    content = '\n'.join(contents)
    #comment = '\n'.join(comments)
    print(content)
    """print("---comment:----------------------")
    print(comment)
    print("------------------------------------------")"""
    """
    coms = root.find_all("span",class_="f3 push-content")
    users = root.find_all("span",class_="f3 h1 push-userid")
    tags = root.find_all("span",class_ ="f1 h1 push-tag" )
    print("---comment:----------------------")
    n=0
    for com in coms:
        print(users[n])
        n=n+1
        print(com.string)
    """
    pushs=root.find_all("div",class_="push")
    #print("---comment:----------------------")
    for push in pushs:
        user = push.find("span",class_="f3 hl push-userid")
        com = push.find("span",class_="f3 push-content")
        #print(user.string)
        #print(push)
        """
        tag = push.find("span",class_="f3 hl push-tag")
        tag = push.find("span", {'class': 'push-tag'}).text
        print(tag.string)
        不知道為甚麼不能用
        """
        tag = push.find("span", {'class': 'push-tag'}).text
        print(tag)
        #print(push.span.string)
        print(user.string)
        if com.a != None:
            print(com.a["href"])
        else:
            print(com.string)



url="https://www.ptt.cc/bbs/Gossiping/index.html"
f = open('gossipingcrawler_test.txt', 'w')
n=0
while n<1:
    url = "http://www.ptt.cc"+ crawl(url)
    n+=1
f.close()

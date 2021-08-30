import json
import urllib.request,urllib.error
import re

def main():
    url = "https://www3.nhk.or.jp/news/json16/new_001.json?_=1630290134358"
    askURL(url)
def askURL(url):
    #建立一個Request物件，附加request haders 的資訊
    #模擬request
    request=urllib.request.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    })
    html=""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("gbk")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
if __name__=="__main__":
    main()

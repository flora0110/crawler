#引入函示庫
import requests, json
import matplotlib.pyplot as plt
#利用get取得API資料
url="https://www.dcard.tw/_api/forums/pet/posts?popular=false"
reqs = requests.get(url)
#利用json.loads()解碼JSON
reqsjson = json.loads(reqs.text)
#利用迴圈儲存男女數值
gender = {"F":0, "M":0}
for content in reqsjson:
    gender[content['gender']]+=1

#利用plt畫長條圖表
kind = ['boy','girl']
data = [gender['F'],gender['M']]
plt.bar(kind ,data)
plt.yticks(range(0, 21, 2))
plt.show()

import requests
import json
import datetime as dt
import line_notify as line
import configparser

#使用ConfigParser套件讀入組態檔
conf = configparser.ConfigParser()
#載入組態檔
conf.read("config.ini", encoding="utf-8")

#Trello Key & Token
key = conf.get('Trello' , 'key')
token = conf.get('Trello' , 'token')
border = conf.get('Trello' , 'border')

#line token
line_token = conf.get('Line' , 'token')

#url = "https://api.trello.com/1/boards/"+border+"?fields=name,url&key="+key+"&token="+token
#取得border資訊
#req = requests.request('GET', url)
#print(req.text)

url = "https://api.trello.com/1/boards/"+border+"/lists?cards=open&card_fields=all&fields=name,url&key="+key+"&token="+token

#取得border裡的卡片清單
req = requests.request('GET', url)
card_lists = json.loads(req.text)
# print(card_lists)

#TODO 未來改成文章截止日，可能是每週日吧！？！
today = dt.datetime.now().strftime("%Y-%m-%d")

users = []
#偵測卡片的due date有沒有截止日的
for lists in card_lists:
    has = False
    for card in lists['cards']:
        #卡片沒設定due的話跳過這一張卡片
        if card['due'] == None:
            continue 
        
        #抓卡片的due date 跟 是否打勾
        if (today == card['due'].split('T')[0]) and (card['dueComplete']):
            has = True
            break
    
    #如果這個列表沒有該週的文章card，記錄下人名
    if not has:
        # print("send notify to "+lists['name'])
        users.append(lists['name'])

#製作訊息
message = {'message': "Hi "+str(users)+",該寫本週的文章了呦～"}
#發送訊息
line.send_notify(line_token, message)


from imports import *
from send_message import *
import csv


def send_generic(recipient_id,text,cost,rid,address):
    a=[]

    # for i in text:
    #     print(str(i))
    x=-1
    data_len=11
    print(address)
    if len(text)<11 :
        data_len=len(text)
    for i in range(0,data_len):
         # print(address)
        a.append(json.dumps({
            "title": text[i],
            "image_url": "https://cdn.pixabay.com/photo/2015/04/08/13/13/food-712665_960_720.jpg",
            "subtitle": "avgcost:"+str(cost[i])+"\n:"+"\n"+"location:"+str(address[i+1][1])+","+str(address[i+1][0]),
            "default_action": {
                "type": "web_url",
                "url": "http://www.ipeen.com.tw/shop/"+str(rid[i]),
                "webview_height_ratio": "tall"
            },
            "buttons": [
                {
                    "title": "more info",
                    "type": "web_url",
                    "url": "http://www.ipeen.com.tw/shop/"+str(rid[i]),
                    "webview_height_ratio": "tall"
                },
                {
                    "title": "how to go",
                    "type": "web_url",
                    "url": "https://www.google.com.tw/maps/dir/"+str(address[0][1])+","+str(address[0][0])+"/"+str(address[i+1][1])+","+str(address[i+1][0]),
                    "webview_height_ratio": "tall"
                },
                # {

                #     "title": "select",
                #     "type": "web_url",
                #     "url": "/send_message",
                #     "webview_height_ratio": "tall"
                # }
            ]
        }))
    data = json.dumps({     
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": a
                }
            }
        }#end message
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
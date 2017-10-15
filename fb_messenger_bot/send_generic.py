from imports import *
import csv


def send_generic(recipient_id,text,cost):
    a=[]

    # for i in text:
    #     print(str(i))
    x=-1
    data_len=11
    if len(text)<11 :
        data_len=len(text)
    for i in range(0,data_len):
        a.append(json.dumps({
            "title": text[i],
            "image_url": "http://iphoto.ipeen.com.tw/photo/ipeen/200x200/def/8/4/8/838848/838848_20150412173830_6101.jpg",
            "subtitle": cost[i],
            "default_action": {
                "type": "web_url",
                "url": "https://dinein.kfc.com.sg/",
                "webview_height_ratio": "tall"
            },
            "buttons": [
                {
                    "title": "more info",
                    "type": "web_url",
                    "url": "https://dinein.kfc.com.sg/",
                    "webview_height_ratio": "tall"
                },
                {
                    "title": "menu",
                    "type": "web_url",
                    "url": "https://dinein.kfc.com.sg/our-food/",
                    "webview_height_ratio": "tall"
                }
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
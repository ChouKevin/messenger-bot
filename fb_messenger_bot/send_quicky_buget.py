from imports import *

def send_quicky_buget(recipient_id):
    a = []
    a.append(json.dumps({
          "content_type":"text",
          "title":"My buget...",
          "payload":"<POSTBACK_PAYLOAD>"
        }))
    for i in range(0,9):
        a.append(json.dumps({
          "content_type":"text",
          "title":str(i*100)+str("~")+str(i*100+100),
          "payload":"<POSTBACK_PAYLOAD>"
        }))
    print(a)
    data = json.dumps({     
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text": "sccc",
            "quick_replies":a
        }
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
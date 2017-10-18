from imports import *

def send_quicky_distance(recipient_id):
    a = []
    for i in range(1,8):
      a.append(json.dumps({
        "content_type":"text",
        "title":":"+str(i*500),
        "payload":"<POSTBACK_PAYLOAD>"
      }))

    data = json.dumps({     
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text": "distance",
            "quick_replies":a
        }
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
from imports import *

def send_quicky(recipient_id,text):
    data = json.dumps({     
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text": text,
            "quick_replies":[
              {
                "content_type":"location"
              },
              {
                "content_type":"text",
                "title":"My buget...",
                "payload":"<POSTBACK_PAYLOAD>"
              },
              {
                "content_type":"text",
                "title":"news",
                "payload":"<POSTBACK_PAYLOAD>"
              },
              {
                "content_type":"text",
                "title":"I want eat...",
                "payload":"<POSTBACK_PAYLOAD>"
              }, 
              {
                "content_type":"text",
                "title":"image",
                "payload":"<POSTBACK_PAYLOAD>"
              },
              {
                "content_type":"text",
                "title":"list",
                "payload":"<POSTBACK_PAYLOAD>"
              }
            ]
        }
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
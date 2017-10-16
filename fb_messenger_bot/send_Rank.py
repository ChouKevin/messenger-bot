from imports import *
import csv


def send_Rank(recipient_id):
    data = json.dumps({     
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text": "rank",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"Excellent",
                "payload":"5",
                "image_url":"http://tuts.ahninniah.graphics/content/images/2014/Jul/crown\_title.png"
              },
              {
                "content_type":"text",
                "title":"Great",
                "payload":"<POSTBACK_PAYLOAD>"
              },
              {
                "content_type":"text",
                "title":"Good",
                "payload":"<POSTBACK_PAYLOAD>"
              },
              {
                "content_type":"text",
                "title":"Dislike",
                "payload":"<POSTBACK_PAYLOAD>"
              },
              {
                "content_type":"text",
                "title":"Hate",
                "payload":"<POSTBACK_PAYLOAD>"
              },
            ]
        }
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
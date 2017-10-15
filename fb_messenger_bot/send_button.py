from imports import *

def send_button(recipient_id, message_text=''):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"button",
                "text":message_text,
                "buttons":[
                  {
                    "type":"web_url",
                    "url":"https://www.starbucks.com.tw/home/index.jspx?r=6",
                    "title":"starbucks"
                  },{
                    "type":"web_url",
                    "url":"http://www.kfcclub.com.tw/",
                    "title":"KFC"
                  }
                ]
              }
            }
        }
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
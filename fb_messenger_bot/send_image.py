from imports import *

def send_image(recipient_id):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
              "type":"image", 
              "payload":{
                "url":"http://iphoto.ipeen.com.tw/photo/ipeen/200x200/vip/3/7/0/store_10073/sp10073_20140818180447471.jpg", 
              }
            }
        },
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
    
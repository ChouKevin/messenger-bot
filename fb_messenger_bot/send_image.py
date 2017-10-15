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
                "url":"http://images5.fanpop.com/image/photos/31300000/beautiful-heart-pic-beautiful-pictures-31395948-600-900.jpg", 
              }
            }
        },
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
    
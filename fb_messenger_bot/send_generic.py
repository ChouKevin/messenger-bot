from imports import *
import csv


def send_generic(recipient_id):
    data = json.dumps({     
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Smurfs: The Lost Village (2017)",
                            "image_url": "http://iphoto.ipeen.com.tw/photo/ipeen/200x200/def/8/4/8/838848/838848_20150412173830_6101.jpg",
                            "subtitle": "KFC landed in Singapore in 1977, when the first restaurant opened its doors at Somerset Road.Today KFC serves more than 1 million customers each month through over 80 stores across Singapore. This makes KFC one of the largest fast food chains in the country.We are passionate about serving our customers freshly prepared, great tasting food with a key part of this being The Colonel's signature blend of 11 herbs and spices. Even today these remain a secret with the original recipe under lock and key in our headquarters in Kentucky, USA.",
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
                        },
                        {
                            "title": "Resident Evil: The Final Chapter (2017)",
                            "image_url": "https://www.moovrika.com/ext/makeimg.php?tbl=movies&id=4167&img=1&type=image&movie=Resident+Evil+The+Final+Chapter&fs=400",
                            "subtitle": "Resident Evil: The Final Chapter is an upcoming science fiction action horror film written and directed by Paul W. S. Anderson. It is the sequel to Resident Evil: Retribution (2012), and will be the sixth and final installment in the Resident Evil film series, which is very loosely based on the Capcom survival horror video game series Resident Evil.",
                            "default_action": {
                                "type": "web_url",
                                "url": "https://www.moovrika.com/m/4167",
                                "webview_height_ratio": "tall"
                            },
                            "buttons": [
                                {
                                    "title": "more info",
                                    "type": "web_url",
                                    "url": "https://www.moovrika.com/m/4082",
                                    "webview_height_ratio": "tall"
                                }
                            ]
                        }
                    ]
                }
            }
        }#end message
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)
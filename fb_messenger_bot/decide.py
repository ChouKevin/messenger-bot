import os
import sys
import json
from settings import *
import logging
import requests
from flask import Flask, request

from send_message import send_message 




def log(message):
    print(str(message))
    sys.stdout.flush()

def send_button(recipient_id, message_text):
    params = {
        "access_token":app_config["PAGE_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
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
                    "url":"https://www.facebook.com/ipeen/",
                    "title":"Visit Messenger"
                  }
                ]
              }
            }
        }
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def send_location(recipient_id, message_text):
    params = {
         "access_token":app_config["PAGE_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
        
    }
    data = json.dumps({
        
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text": "Here's a quick reply!",
            "quick_replies":[
              {
                "content_type":"text",
                "title":message_text,
                "payload":"<POSTBACK_PAYLOAD>",
                "image_url":"http://example.com/img/red.png"
              },
              {
                "content_type":"location",
                "image_url":"http://example.com/img/red.png"
              },
              {
                "content_type":"text",
                "title":"Something Else",
                "payload":"<POSTBACK_PAYLOAD>"
              }
            ]
        }
    })
    r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)



class decide(object):
    """docstring for Decide"""
    def __init__(self):
        pass
    def process(self, request):
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        if "text" not in messaging_event["message"]:
                            diction = dict()
                            for attachments in messaging_event["message"]["attachments"]:
                                diction[sender_id]=attachments["payload"]["coordinates"]
                                print(diction[sender_id],sender_id)
                            send_message(sender_id, "location finished")
                        else:
                            message_text = messaging_event["message"]["text"]  # the message's text
                            #send_message(sender_id, decide.deal(message_text) + 'deeal')
                            if message_text == "hi":
                                send_message(sender_id, "hello")
                            elif message_text == "!":
                                send_location(sender_id, "where")
                            elif message_text == "news":
                                send_button(sender_id, "this is news")
                            else :
                                send_message(sender_id, "we don not understand this text @by admin:"+message_text)
                    if messaging_event.get("delivery"):# delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass

    def deal(self, text):
        return text
    
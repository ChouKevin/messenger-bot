import json
from settings import *
import requests

class SendQuick(object):
    def __init__(self, recipient_id):
        self.recipient_id = recipient_id

    def send_main_replies(self, text):
        content_type = ['text', 'location', 'text', 'text', 'text']
        title = ['search', 'my location', 'distance', 'My budget...', 'I want eat...']
        self.send(content_type, title, text)

    def send_distance(self, text='set your distance range:'):
        distance = []
        content_type = []
        for i in range(0,9):
            distance.append(str(i*500))
            content_type.append('text')
        self.send(content_type, distance, text)

    def send_interval_cost(self, text='set your budget: xxx-xxx'):
        cost = []
        content_type = []
        for i in range(0,9):
            cost.append(str(i*100)+'-'+str(i*100+100))
            content_type.append('text')
        self.send(content_type, cost, text)

    def send(self, content_type, title, text):
        header = self.create_header(text)
        quick_replies = self.create_quick_replies(content_type, title)
        header['message'].update(quick_replies)
        data = json.dumps(header)
        r=requests.post("https://graph.facebook.com/v2.6/me/messages", params=app_config["PARAMS"], headers=app_config["HEADERS"], data=data)

    def create_quick_replies(self, content_type, title):
        """input: list; output: "quick_replies":[]"""
        quick_replies = {'quick_replies':[]}
        for i in range(len(content_type)):
            quick_replies['quick_replies'].append(
                {
                    'content_type': content_type[i],
                    'title': title[i],
                    "payload": "<POSTBACK_PAYLOAD>"
                }
            )
        return quick_replies

    def create_header(self, text=''):
        header = {
            'recipient':{
                'id': self.recipient_id
            },
            'message':{
                'text':text
            }
        }
        return header
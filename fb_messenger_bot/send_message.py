import os
import sys
import json
from settings import *
import logging
import requests
from flask import Flask, request


def send_message(recipient_id, message_text):
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
        "message": {
            "text": message_text
        },

    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
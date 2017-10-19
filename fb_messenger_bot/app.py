from decide import decide
from flask import Flask, request, redirect, url_for
from settings import *
from mongoengine import *
from imports_send import *
from sendQuick import SendQuick
from send_quicky import *
from controller import *
import json

app = Flask(__name__)
decide = decide()
#r=requests.post('')
sq = SendQuick()
dl = dealMessage.DealMessage('')

register_connection(
    alias='default',
    name = db_config['DB'],
    host = db_config['HOST'],
    port = db_config['PORT'],
    username = db_config['USER'],
    password = db_config['PASSWD'],
    authentication_source = 'admin'
    )

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == app_config['WEBHOOK']: #os.environ[]: "VERIFY_TOKEN"
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    # code=307 > POST  code=302 > GET
    print('root')
    result = decide.parse_request(request)
    if result is not None:
        sq.set_sender_id(result['sender_id'])
        dl.sender = result['sender_id']
        if result['code'] == 307 :
            return redirect(url_for(result['path'], sender_id=result['sender_id'], data=result['data'], value=result['value']), code=result['code'])
        else:
            return redirect(url_for(result['path'], sender_id=result['sender_id'], data=result['data'], value=result['value']))
    return "ok", 200

@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'GET':
        sq.send_main_replies(request.args.get('data'))
    else :
        sq.send_main_replies('i got it')
    return 'ok', 200

@app.route('/rate', methods=['GET', 'POST'])
def rate():
    print('rate')
    rid = request.args.get('rid', default=None, type=int)
    uid = request.args.get('uid', default=None, type=str)
    return 'ok', 200

@app.route('/distance', methods=['GET', 'POST'])
def distance():
    if request.method == 'GET':
        sq.send_distance(request.args.get('data'))
    else :
        dl.set_distance(request.args.get('value'))
        sq.send_main_replies('i got it')
    return 'ok', 200

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    print('budget')
    if request.method == 'GET':
        sq.send_interval_cost()
    else :
        sq.send_main_replies('i got it')
    return 'ok', 200

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    print('budget')
    if request.method == 'GET':
        sq.send_main_replies('to be continue')
    else :
        sq.send_main_replies('i got it')
    return 'ok', 200

@app.route('/nothing', methods=['GET', 'POST'])
def nothing():
    sq.send_main_replies(request.args.get('data'))
    return 'ok', 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
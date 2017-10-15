from decide import decide
from flask import Flask, request, redirect, url_for
from settings import *
from mongoengine import *

app = Flask(__name__)
decide = decide()
#r=requests.post('')



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

# (int, int)
@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    decide.process(request)
    return "ok", 200

@app.route('/', methods=['GET'])
def process():
    print(request.args.get('data')) #123

@app.route('/rate', methods=['GET'])
def rate():
    rid = request.args.get('rid', default=None, type=int)
    uid = request.args.get('uid', default=None, type=str)
    print(rid, uid)
    return redirect(url_for('process', data=123)) #url = /?data=123
    # return redirect(url_for('process', data=123, code=307)) #code307 >> POST
    # http://funhacks.net/2016/10/05/flask_redirect/

if __name__ == '__main__':
    app.run(debug=True)
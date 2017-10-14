from decide import decide
from flask import Flask, request
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

if __name__ == '__main__':
    app.run(debug=True)
from imports_send import *
from model.restaurant import *
from controller.dealMessage import *
from flask import redirect, url_for, request
from settings import *
from sendQuick import *
from controller.userRate import *
import re

restaurant=Restaurant()


def log(message):
    print(str(message))
    sys.stdout.flush()

class decide(object):
    """docstring for Decide"""

    def parse_request(self, data, session):
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        dealMessage = DealMessage(sender_id)
                        if dealMessage.search_sender(sender_id) is None:
                            return {'path':'location', 'sender_id':sender_id, 'data': 'please input your location to be our user' }
                        if "text" not in messaging_event["message"]:
                            pass
                        else:
                            message_text = messaging_event["message"]["text"]
                            path = self.decide_action(message_text, dealMessage.get_user_stauts())
                            dealMessage.set_user_status(path)
                            data = self.decide_talk(path)
                            return {'path':path, 'sender_id':sender_id, 'data': data}
    
    def is_number_intervel(self, text):
        pass

    
    def decide_action(self, message_text, status):
        path = None
        if status == 'nothing':
            if message_text == "I want eat...": 
                send_message(sender_id, "what do you wanna eat?")
            elif message_text == "restaurant catalog":
                send_message(sender_id, "this is your catalog")
            elif message_text == "search":
                path = 'search'
            elif message_text == "My budget...":
                path = 'budget'
            elif message_text == "distance":
                path = 'distance'
            elif message_text == 'rate':
                path = 'rate'
            else:
                path = 'nothing'
        else:
            path = status
        return path

    def decide_talk(self, action):
        talk = None
        if action == 'search':
            talk = 'your search result is:'
        elif action == "restaurant catalog":
            talk = ''
        elif action == 'budget':
            talk = 'input your budget (xxx-xxx):'
        elif action == 'rate':
            talk = 'input your score:'
        elif action == 'distance':
            talk = 'input your distance:'
        elif action == 'nothing':
            talk = "we do not know this text,\nHere's a quick reply!"
        return talk


    def process(self, request):
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:

                for messaging_event in entry.get("messaging",[]):
                    quick_text="anymore action?"
                    isquicky=True
                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        dealMessage=DealMessage(sender_id)
                        #new code 
                        sendQuick=SendQuick(sender_id)
                        if dealMessage.search_sender(sender_id) is None:
                            print('not find sender')
                            return {'path':'location', 'sender_id':sender_id, 'data': 'please input your location to apply for user' }

                        if "text" not in messaging_event["message"]:
                            typeText=""
                            for attachments in messaging_event["message"]["attachments"]:
                                    typeText=attachments["type"]
                            if typeText== "location":
                                diction = dict()
                                for attachments in messaging_event["message"]["attachments"]:
                                    diction[sender_id]=attachments["payload"]["coordinates"]
                                print(diction[sender_id],sender_id)
                                location_tuple=(diction[sender_id]['long'],diction[sender_id]['lat'])
                                source=dealMessage.search_sender(sender_id)
                                # dealMessage.set_cost(source.cost[0],source.cost[1])
                                dealMessage.set_distance(source.distance)
                                dealMessage.set_location(location_tuple)
                                dealMessage.save_search_set()
                                send_message(sender_id,str(location_tuple))
                                send_message(sender_id, "location finished")

                        else:
                            message_text = messaging_event["message"]["text"]  # the message's text
                            if message_text == "I want eat...": 
                                send_message(sender_id, "what do you wanna eat?")
                            
                            elif message_text == "restaurant catalog":
                                send_message(sender_id, "this is your catalog")
                            elif message_text =="search":
                                source=dealMessage.search_sender(sender_id)
                                dealMessage.set_cost(source.cost[0],source.cost[1])
                                dealMessage.set_distance(source.distance)
                                dealMessage.save_search_set()
                                text=[]
                                cost=[]
                                rid=[]
                                address=[]
                                imgUrl=[]
                                address.append(source.location['coordinates'])

                                print("decide line 75:")
                                for i in dealMessage.get_restaurant():
                                    text.append(i.name)
                                    cost.append(i.avgCost)
                                    rid.append(i.rid)
                                    address.append(i.address['coordinates'])
                                    imgUrl.append(dealMessage.get_rid_image(i.rid))
                                    print(imgUrl)
                                if len(text) == 0:
                                    send_message(sender_id,"no result")
                                else :
                                    send_generic(sender_id,text,cost,rid,address,imgUrl)

                            elif message_text=="Rank":#rank
                                isquicky=False
                                send_Rank(sender_id)
                            elif message_text == "My budget...":
                                isquicky=False
                                #send_quicky_buget(sender_id)
                                sendQuick.send_interval_cost()
                            elif message_text == "distance":
                                isquicky=False
                                sendQuick.send_distance()
                                # send_quicky_distance(sender_id)
                            elif '-' in message_text : #cost
                                source=dealMessage.search_sender(sender_id)
                                under,upper= message_text.split("-")
                                print(under,upper)
                                dealMessage.set_distance(source.distance)
                                dealMessage.set_cost(under,upper)
                                dealMessage.save_search_set()

                            elif ':' in message_text:# distance
                                key,value= message_text.split(":")
                                send_message(sender_id,"your distance:"+str(value))
                                source=dealMessage.search_sender(sender_id)
                                
                                source=dealMessage.search_sender(sender_id)
                                dealMessage.set_cost(source.cost[0],source.cost[1])
                                dealMessage.set_distance(value)
                                dealMessage.save_search_set()
                                dealMessage.set_distance(value)
                                dealMessage.save_search_set()
                            else :
                                quick_text="we do not know this text:\n"+message_text+"\nHere's a quick reply!"
                        # dealMessage.save_search_set()
                        if isquicky:
                            # send_quicky(sender_id,quick_text)
                            sendQuick.send_main_replies(quick_text)
                                
                    if messaging_event.get("delivery"):# delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        title = messaging_event["postback"]["title"]

                        rest_id = messaging_event["postback"]["payload"]
                        sender_id = messaging_event["sender"]["id"]
                        userRate=UserRate(sender_id)
                        userRate.rate_restaurant()
                        send_message(sender_id,"!@#")

                # for messaging_event in entry.get("standby",[]):
                   



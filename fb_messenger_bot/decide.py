from imports_send import *
from model.restaurant import *
from controller.dealMessage import *
from flask import redirect, url_for
from settings import *

restaurant=Restaurant()

def log(message):
    print(str(message))
    sys.stdout.flush()

class decide(object):
    """docstring for Decide"""
    def __init__(self):
        pass
    def process(self, request):
        data = request.get_json()
        
        location_tuple=(0,0)
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    quick_text="anymore action?"
                    isquicky=True
                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        dealMessage=DealMessage(sender_id)

                        
                        if dealMessage.search_sender(sender_id) is None:
                            print('not find sender')
                            return {'path':'location', 'sender_id':sender_id, 'data':u"請輸入座標"}
                            # return redirect(url_for('location', sender_id=sender_id, data=u"請輸入座標"))

                        if "text" not in messaging_event["message"]:
                            typeText=""
                            for attachments in messaging_event["message"]["attachments"]:
                                    typeText=attachments["type"]
                            print(typeText)
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
                            elif message_text =="Result!!":
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
                                send_quicky_buget(sender_id)
                            elif message_text == "distance":
                                isquicky=False
                                send_quicky_distance(sender_id)
                            elif '~' in message_text : #cost
                                source=dealMessage.search_sender(sender_id)
                                under,upper= message_text.split("~")
                                print(under,upper)
                                dealMessage.set_distance(source.distance)
                                dealMessage.set_cost(under,upper)
                                dealMessage.save_search_set()

                            elif ':' in message_text:# distance

                                send_message(sender_id,"distance"+str())
                                print("distance:"+str(sender_id))
                                source=dealMessage.search_sender(sender_id)
                                print(type(source))
                                key,value= message_text.split(":")
                                source=dealMessage.search_sender(sender_id)
                                dealMessage.set_cost(source.cost[0],source.cost[1])
                                dealMessage.set_distance(value)
                                dealMessage.save_search_set()
                                dealMessage.set_distance(value)
                                dealMessage.save_search_set()
                            # # just testing function 
                            # elif message_text == "news":
                            #     dealMessage.set_distance
                                # send_button(sender_id, "this is news location we recommend")
                            # elif message_text =='image':
                            #     send_image(sender_id)
                            # elif message_text == 'list':
                            #     send_generic(sender_id)
                            else :
                                quick_text="we do not know this text:\n"+message_text+"\nHere's a quick reply!"
                        # dealMessage.save_search_set()
                        if isquicky:
                            send_quicky(sender_id,quick_text)
                                
                    if messaging_event.get("delivery"):# delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
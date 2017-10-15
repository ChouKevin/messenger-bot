from imports_send import *
from model.restaurant import *
from controller.dealMessage import *
import pymongo

client= pymongo.MongoClient(host=settings.host,port=settings.port)
# db=client.
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
                                print(location_tuple[0])
                                dealMessage.set_distance(1500)
                                dealMessage.set_location((location_tuple[0],location_tuple[1]))
                                send_message(sender_id,str(location_tuple)+"aaaaa")
                                text=[]
                                cost=[]
                                for i in dealMessage.get_restaurant():
                                    text.append(i.name)
                                    cost.append(i.avgCost)
                                send_generic(sender_id,text,cost)
                                print(cost)
                                    # print(str(i.name))
                                    # print("==================")
                                print("text append"+str(text))
                                    # send_message(sender_id,str(i.name))
                                
                                send_message(sender_id, "location finished")

                            #elif typeText=="image":

                        else:
                            message_text = messaging_event["message"]["text"]  # the message's text
                            
                            if message_text == "I want eat...": 
                                send_message(sender_id, "what do you wanna eat?")
                            elif message_text == "My buget...":
                                isquicky=False
                                send_quicky_buget(sender_id)
                            elif message_text == "restaurant catalog":
                                send_message(sender_id, "this is your catalog")
                            elif '~' in message_text :
                                under,upper= message_text.split("~")
                                # dealMessage.set_location((121.56008359778, 25.080193176667))
                                print("is get location ?"+str(location_tuple[0]))
                                dealMessage.set_location((location_tuple[0],location_tuple[1]))
                                dealMessage.set_cost(under,upper)
                                for i in dealMessage.get_restaurant():
                                    print(i.name)
                                text=[]
                                cost=[]
                                for i in dealMessage.get_restaurant():
                                    text.append(i.name)
                                    cost.append(i.avgCost)
                                send_generic(sender_id,text,cost)
                                send_message(sender_id,"got $$"+under)
                            elif ':' in message_text:
                                key,value= message_text.split(":")
                            # # just testing function 
                            # elif message_text == "news":
                            #     dealMessage.set_distance
                                # send_button(sender_id, "this is news location we recommend")
                            elif message_text =='image':
                                send_image(sender_id)
                            # elif message_text == 'list':
                            #     send_generic(sender_id)
                            else :
                                quick_text="we do not know this text:\n"+message_text+"\nHere's a quick reply!"

                        if isquicky:
                            send_quicky(sender_id,quick_text)
                                
                    if messaging_event.get("delivery"):# delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
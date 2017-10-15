from imports_send import *
from model.restaurant import *
from controller.dealMessage import *
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
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    quick_text="anymore action?"
                    isquicky=True
                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        if "text" not in messaging_event["message"]:
                            typeText=""
                            for attachments in messaging_event["message"]["attachments"]:
                                    typeText=attachments["type"]
                            print(typeText)
                            if typeText== "location":
                                diction = dict()
                                dealMessage=DealMessage(sender_id)
                                dealMessage.set_location((121.56008359778, 25.080193176667))
                                for attachments in messaging_event["message"]["attachments"]:
                                    diction[sender_id]=attachments["payload"]["coordinates"]
                                print(diction[sender_id],sender_id)
                                location_tuple=(diction[sender_id]['long'],diction[sender_id]['lat'])
                                send_message(sender_id,str(location_tuple))
                                for i in dealMessage.get_restaurant():
                                    print(str(i.name))
                                    send_message(sender_id,str(i.name))
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
                            #just testing function 
                            # elif message_text == "news":
                            #     send_button(sender_id, "this is news location we recommend")
                            elif message_text =='image':
                                send_image(sender_id)
                            elif message_text == 'list':
                                send_generic(sender_id)
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
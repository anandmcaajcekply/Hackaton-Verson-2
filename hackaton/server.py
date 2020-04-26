from bot import telegram_chatbot
import gizoogle
import re
import json
from urllib.parse import urlparse

bot = telegram_chatbot("config.cfg")


def IsTrustedURL(msg):
	# JSON file 
	f = open ('trustedURL.json', "r") 
	  
	# Reading from file 
	data = json.loads(f.read()) 
	
	parsed_uri = urlparse(msg)
	uri = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)	
	
	if data and uri in data: # test for emptiness and for membership
		return "This news is from a trusted source" 
	else:
		return "This news is not from a trusted source"
	  
	# Closing file 
	f.close() 



def Find(msg): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg) 
    return bool(url)
	
def make_reply(msg):
	reply = None
	a = Find(msg)
	if a == 1:
		result = IsTrustedURL(msg)
		return result
	elif a == 0:
		reply = msg
		return reply

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            reply = make_reply(message)
            bot.send_message(reply, from_)

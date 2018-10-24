#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by Şükrü Ozan, Ph.D. 24.10.2018

import json 
import requests
import time
import python_forex_quotes # Should be seperately installed

TOKEN = "<your-telegram-bot-api-token>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
client = python_forex_quotes.ForexDataClient('<your-forex-quotes-api-token>')

# Get symbols to be used. Eg. 'EURTRY' gives Turkish Lira equivalent of 1 EURO
symbols = client.getSymbols()

# These functions are necessary to run your bot by using HTTP POST requests
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates():
    url = URL + "getUpdates?limit={}&offset={}".format("10", "-1") 
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    message_id = updates["result"][last_update]["message"]["message_id"]
    return (text, chat_id, message_id)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)    

def send_message(text, chat_id, parse='HTML'):
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode={}".format(text, chat_id,parse)
    get_url(url)

def reply_message(text, chat_id, message_id):
    url = URL + "sendMessage?text={}&reply_to_message_id={}&chat_id={}".format(text,message_id,chat_id)
    get_url(url)

# Main loop
def main():
	try:
		updates = get_updates()
		last_update_id = get_last_update_id(updates)
		wait = 5.0
		send_message("<b> BOT STARTED </b>",'<your-telegram-chad-id>', 'HTML')
		while True:
			updates = get_updates()
			update_id = get_last_update_id(updates)
			# print(last_update_id, update_id,wait)
			
			if update_id != last_update_id :
				last_update_id = update_id					
				text, chat_id, message_id = get_last_chat_id_and_text(updates)			
				wordlist = text.split()
				
				quote_list = []
				for word in wordlist:
					if  word.upper() in symbols:
						quote_list.append(word.upper())
				
				if len(quote_list)>0:
					response = client.getQuotes(quote_list)
					message = "<b>"
					for result in response:
						message +=  str(result['symbol'])+":"+str(result['price'])+"\n"
					message += "</b>"
					send_message(message, chat_id,'HTML')	
					send_message("<b> A REQUEST HAS BEEN MADE! </b>",'<your-telegram-chad-id>', 'HTML')
					
					wait = 5.0			
			time.sleep(wait)
			wait += 1.0
			wait =wait%30

	except:
		send_message("<b> BOT TERMINATED! </b>",'<your-telegram-chad-id>', 'HTML')
		

if __name__ == '__main__':
    main()

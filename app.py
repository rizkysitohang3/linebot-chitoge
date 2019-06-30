import os
import re
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

from decouple import config
from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)




app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)


    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
	message = str.lower(event.message.text).strip()
	whitelist = string.ascii_letters + string.digits + ' '
	message = ''.join(c for c in message if c in whitelist)
	message = message.split()
	
	if message[0] == 'jadwal' :
				
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=jadwal(message[1] if len(message)>1 else ""))
	)
		
		
	elif message[0] == 'now' or message[0] == 'sekarang' or message[0] == 'today':
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=today_time())
	)
	
	elif message[0] == 'hai' or message[0] == 'haii' or message[0] == 'haiii':
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="iyaa\nHaii juga!")
	)
	
	elif message[0] == 'halo' or message[0] == 'haloo' or message[0] == 'halooo':
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="iyaa\nHaloo juga!")
	)
	
	elif message[0] == 'oi' or message[0] == 'oii' or message[0] == 'woii' or message[0] == 'woi':
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="Haaa?\nApaa?")
	)
		
	else :
		
		line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Maaf aku gabisa ngertiin kamu :'\nHiks:'")
    )
    
    


def jadwal(hari):
	text = "jadwal apa ? yg jelas dulu kau kampret"
	
	if hari == "sekarang":
		hari = hari_sekarang()
	elif hari == "besok":
		hari = hari_besok()
	elif hari == "semalam" or hari == "kemarin":
		hari = hari_kemarin()
		
	
	
	
	
	if hari == 'senin':
		text = "Senin :\nNot set yett!"
	elif hari == 'selasa':
		text = "Selasa :\nNot set yett!"
	elif hari == 'rabu':
		text = "Rabu :\nNot set yett!"
				
	elif hari == 'kamis':
		text = "Kamis :\nNot set yett!"		
	elif hari == 'jumat':
		text = "Jumat :\nNot set yett!"
				
	elif hari == 'sabtu':
		text = "Free yay! \neh.. nugas deng :'"
		
	elif hari == 'minggu':
		text = "Gereja kau kampret"
		
	
		
		
	return text

def today_time():
	today = datetime.now() + timedelta(hours=7)
	text =  today.strftime("%A, %d %B %Y ") +" - " + today.strftime(" %H:%M")
	if today.strftime("%d") == "1" :
		text += "\nIt's " + today.strftime("%B! \nSemoga apa-apa yang diingini.\nTeramini.")
		
	return text
	
	
def hari_sekarang():
	today = datetime.now() + timedelta(hours=7)
	wd=date.weekday(today)
	days= ["senin","selasa","rabu","kamis","jumat","sabtu","minggu"]
	return days[wd]


def hari_besok():
	today = datetime.now() + timedelta(hours=7)
	wd=date.weekday(today)
	days= ["senin","selasa","rabu","kamis","jumat","sabtu","minggu"]
	return days[(wd+1) % 7]	
	
def hari_kemarin():
	today = datetime.now() + timedelta(hours=7)
	wd=date.weekday(today)
	days= ["senin","selasa","rabu","kamis","jumat","sabtu","minggu"]
	return days[(wd + 6) % 7]	
		
	
	
	
	
	

    
    
    
   



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

import os
from datetime import date
from datetime import time
from datetime import datetime

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
	
	message = message.split(" ")
	
	if message[0] == 'jadwal' :
				
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=jadwal(message[1]))
	)
		
		
	elif message[0] == 'now' or message[0] == 'sekarang' or message[0] == 'today':
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=today_time)
	)
		
	else :
		
		line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Maaf aku gabisa ngertiin kamu :'\nHiks:'")
    )
    
    


def jadwal(hari):
	text = "jadwal apa ? yg jelas dulu kau kampret"
	if hari == 'senin':
		text = "Not set yett!"
	elif hari == 'selasa':
		text = "Not set yett!"
	elif hari == 'rabu':
		text = "Not set yett!"
				
	elif hari == 'kamis':
		text = "Not set yett!"		
	elif hari == 'jumat':
		text = "Not set yett!"
				
	elif hari == 'sabtu':
		text = "Free yay! \neh.. nugas deng :'"
		
	elif hari == 'minggu':
		text = "Gereja kau kampret"
		
		
	return text

def today_time
	today = datetime.now()
	text =  today.strftime("%A, %d %B %Y ") +" - " + today.strftime(" %H:%M")
	if today.strftime("%d") == "1" :
		text += "\nWelcome " + today.strftime("%B! \nSemoga apa-apa yang diingini.\nTeramini.")
		
	return text
	
	
	
	
	

    
    
    
   



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

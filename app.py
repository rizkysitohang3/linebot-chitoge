import os
import string
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date

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

task_list = []
jadwal_senin = []
jadwal_selasa = []
jadwal_rabu = []
jadwal_kamis = []
jadwal_jumat = []
jadwal_sabtu = []
jadwal_minggu = ['Gereja y.']


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
	message = str.lower(event.message.text).strip()
	whitelist = string.ascii_letters + string.digits + ' '
	message = ''.join(c for c in message if c in whitelist)
	message = message.split()
	
	if message[0] == 'jadwal' :
		if ((message[1] == 'tambah' or message[1] == 'add') if len(message)>1 else False):
			line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=add_jadwal(message[2] if len(message)>2 else "",(' '.join(message[3:])) if len(message)>3 else "" ))
		)
			
			
		elif ((message[1] == 'hapus' or message[1] == 'remove') if len(message)>1 else False) :
			line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=remove_jadwal(message[2] if len(message)>2 else "",(' '.join(message[3:])) if len(message)>3 else "" ))
		)
			
		else:
			line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=jadwal(message[1] if len(message)>1 else ""))
		)
			
		
		
		 		
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
		TextSendMessage(text="o")
	)
	
	elif message[0] == 'halo' or message[0] == 'haloo' or message[0] == 'halooo':
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="oh")
	)
	
	elif message[0] == 'oi' or message[0] == 'oii' or message[0] == 'woii' or message[0] == 'woi':
		line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="Y\nAp?")
	)
		
	else :
		
		line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="G tw.\nNeh cara make:\n- jadwal [sekarang/besok/semalam]\n- jadwal [hari]\n- [now/sekarang/today]\n- jadwal [tambah/add] [hari/task] [teks jadwal]\n- jadwal [hapus/remove] [hari/task] [jadwal]")
    )
    
    


def jadwal(hari):
	
	if libur():
		return "Masih libur elah."
	
	
	
	text = "jadwal apaan? g tw."
	
	if hari == "sekarang":
		hari = hari_sekarang()
	elif hari == "besok":
		hari = hari_besok()
	elif hari == "semalam" or hari == "kemarin":
		hari = hari_kemarin()
		
	
	
	if hari == 'senin':
		text = "Senin :\n"
		if len(jadwal_senin)>0:
			text += '\n'.join(jadwal_senin)
		else:
			text += "G ad."
			
		
		
		
	elif hari == 'selasa':
		text = "Selasa :\n"
		if len(jadwal_selasa)>0:
			text += '\n'.join(jadwal_selasa)
		else:
			text += "G ad."
		
	elif hari == 'rabu':
		text = "Rabu :\n"
		if len(jadwal_rabu)>0:
			text += '\n'.join(jadwal_rabu)
		else:
			text += "G ad."
				
	elif hari == 'kamis':
		text = "Kamis :\n"
		if len(jadwal_kamis)>0:
			text += '\n'.join(jadwal_kamis)
		else:
			text += "G ad."
		
	elif hari == 'jumat':
		text = "Jumat :\n"
		if len(jadwal_jumat)>0:
			text += '\n'.join(jadwal_jumat)
		else:
			text += "G ad."
		
				
	elif hari == 'sabtu':
		text = "Sabtu :\n"
		if len(jadwal_sabtu)>0:
			text += '\n'.join(jadwal_sabtu)
		else:
			text += "G ad."
		
		
	elif hari == 'minggu':
		text = "Minggu :\n"
		if len(jadwal_minggu)>0:
			text += '\n'.join(jadwal_minggu)
		else:
			text += "G ad."
		
		
		
	return text

def today_time():
	today = datetime.now() + timedelta(hours=7)
	text =  today.strftime("%A, %d %B %Y ") +" - " + today.strftime(" %H:%M")
	if today.strftime("%d") == "01" :
		text += "\nSkrg awal" + today.strftime("%B. \nSemngt.\nSemoga apa-apa yang diingini...\nTeramini.")
		
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
		
	
def libur():
	today = datetime.date.today() + timedelta(hours=7)
	start_libur = datetime.date(2019,6,1)
	end_libur = datetime.date(2019,9,1)
	return True if start_libur <= today <= end_libur else False
	

def add_jadwal(hari,text):		
		
	if text == "":
		return "Jadwal ap?\nNeh cara make : jadwal [tambah/add] [hari/task] [teks jadwal]"
	
	if hari == 'senin':
		add_jadwal_senin(text)
		
	elif hari == 'selasa':
		add_jadwal_selasa(text)
	elif hari == 'rabu':
		add_jadwal_rabu(text)
				
	elif hari == 'kamis':
		add_jadwal_kamis(text)
	elif hari == 'jumat':
		add_jadwal_jumat(text)
				
	elif hari == 'sabtu':
		add_jadwal_sabtu(text)
		
	elif hari == 'minggu':
		add_jadwal_minggu(text)
		
	elif hari == 'task':
		add_task_list(text)
	
	else:
		return "Jadwal untuk ap? kpn?\nNeh cara make : jadwal [tambah/add] [hari/task] [teks jadwal]"
	
	return "Ok."


def remove_jadwal(hari,text):		
		
	if text == "":
		return "Hapus Jadwal ap?\nNeh cara make : jadwal [hapus/remove] [hari/task] [teks jadwal]"
	
	if hari == 'senin':
		remove_jadwal_senin(text)
		
	elif hari == 'selasa':
		remove_jadwal_selasa(text)
	elif hari == 'rabu':
		remove_jadwal_rabu(text)
				
	elif hari == 'kamis':
		remove_jadwal_kamis(text)
	elif hari == 'jumat':
		remove_jadwal_jumat(text)
				
	elif hari == 'sabtu':
		remove_jadwal_sabtu(text)
		
	elif hari == 'minggu':
		remove_jadwal_minggu(text)
		
	elif hari == 'task':
		remove_task_list(text)
	
	else:
		return "Hapus Jadwal untuk ap? kpn?\nNeh cara make : jadwal [hapus/remove] [hari/task] [teks jadwal]"
	
	return "Ok.\nKalo ad pasti d hpus."

	
def add_jadwal_senin(text):
	jadwal_senin += text
	
	
def add_jadwal_selasa(text):
	jadwal_selasa += text
	
def add_jadwal_rabu(text):
	jadwal_rabu += text
	
def add_jadwal_kamis(text):
	jadwal_kamis += text
	
	
def add_jadwal_jumat(text):
	jadwal_jumat += text
	
def add_jadwal_sabtu(text):
	jadwal_sabtu += text
	
def add_jadwal_minggu(text):
	jadwal_minggu += text
	
def add_task_list(text):
	task_list += text
	
	

def remove_jadwal_senin(text):
	jadwal_senin = [w for w in jadwal_senin if w != text]
	
	
def remove_jadwal_selasa(text):
	jadwal_selasa = [w for w in jadwal_selasa if w != text]
	
def remove_jadwal_rabu(text):
	jadwal_rabu = [w for w in jadwal_rabu if w != text]
	
def remove_jadwal_kamis(text):
	jadwal_kamis = [w for w in jadwal_kamis if w != text]
	
	
def remove_jadwal_jumat(text):
	jadwal_jumat = [w for w in jadwal_jumat if w != text]
	
def remove_jadwal_sabtu(text):
	jadwal_sabtu = [w for w in jadwal_sabtu if w != text]
	
def remove_jadwal_minggu(text):
	jadwal_minggu = [w for w in jadwal_minggu if w != text]
	
def remove_task_list(text):
	task_list = [w for w in task_list if w != text]
	
	
	

    
    
    
   



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

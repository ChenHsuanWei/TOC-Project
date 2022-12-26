import os
from pyexpat import model

from transitions.extensions import GraphMachine
from utils import send_text_message
import requests
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction, FlexSendMessage

import template

mode=1

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def is_going_to_main(self,event):
        text = event.message.text
        if(text=='寶~在嗎'or text =="喔喔好吧" or text=="好吧XD"):
            return True
 
    def is_going_to_hello(self,event):
        text = event.message.text
        return text == "寶❤️"
    
    def is_going_to_happy(self,event):
        text = event.message.text
        return text == "我今天超開心的ㄟ 你呢"
    
    def is_going_to_EMO(self,event):
        text = event.message.text
        return text == "好煩 今天超emo的..."
    
    def is_going_to_chooseEmo(self,event):
        text = event.message.text
        return text=='我跟你說喔'
    
    def is_going_to_chooseTime(self,event):
        text = event.message.text
        return text=='寶❤️'
    
    def is_going_to_morning(self,event):
        text = event.message.text
        return text=='早安~'
    
    def on_enter_morning(self,event):
        send_text_message(event.reply_token, '早安安\n😊😊')
        send_text_message(event.reply_token, '😊😊')
        reply_token = event.reply_token
        message = template.main
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def is_going_to_afternoon(self,event):
        text = event.message.text
        return text=='午安'
    
    def on_enter_afternoon(self,event):
        send_text_message(event.reply_token, '午安 你吃飽了嗎~')
        send_text_message(event.reply_token, '你吃飽了嗎~')
        reply_token = event.reply_token
        message = template.main
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def is_going_to_night(self,event):
        text = event.message.text
        return text=='晚安💤'
    
    def is_going_to_reject1(self,event):
        text = event.message.text
        return text=='你願意和我交往嗎🥺'
    
    def is_going_to_reject2(self,event):
        text = event.message.text
        return text=='寶 願不願意給我們一個交往的機會'
    
    def on_enter_reject2(self,event):
        #send_text_message(event.reply_token, '我希望你搞清楚 搞清楚我們只是朋友')
        mode=0
        reply_token = event.reply_token
        message = template.reject2
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        
    def on_enter_reject1(self,event):
        #send_text_message(event.reply_token, '我暫時不想交男友ㄟ...但我們還是朋友啦')
        mode=0
        reply_token = event.reply_token
        message = template.reject1
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        

    def on_enter_night(self,event):
        send_text_message(event.reply_token, '寶晚安\n祝你有個好夢ZZZZ')
        #push_message(userid, '祝你有個好夢ZZZZ')
        send_text_message(event.reply_token, '祝你有個好夢XDDD')
        reply_token = event.reply_token
        message = template.main
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()
    
    def on_enter_chooseTime(self,event):
        reply_token = event.reply_token
        message = template.chooseTime
        message_to_reply = FlexSendMessage("選擇高濃度", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
    
    def on_enter_happy(self,event):
        send_text_message(event.reply_token, '哈哈 我也是╰(*°▽°*)╯')
        reply_token = event.reply_token
        message = template.main
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_EMO(self,event):
        send_text_message(event.reply_token, '沒事啦')
        send_text_message(event.reply_token, '給你拍拍')
        reply_token = event.reply_token
        message = template.main
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_chooseEmo(self,event):
        reply_token = event.reply_token
        message = template.chooseEmo
        message_to_reply = FlexSendMessage("選擇高濃度", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
    
    def on_enter_main(self,event):
        reply_token = event.reply_token
        message = template.main
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def is_going_to_confess(self,event):
        text=event.message.text
        return text=="我們在一起好不好🥺"
    
    #model.get_graph().draw('fsm.png', prog='dot')
    
    

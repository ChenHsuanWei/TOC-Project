import os
from pyexpat import model
import sys
import graphviz

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=[
        #'input_age',
        #'input_gender',
        'user',
        'main',
        'confess',
        'chooseEmo',
        'happy',
        'EMO',
        'chooseTime',
        'morning',
        'afternoon',
        'night',
        'reject1',
        'reject2'
    ],
    transitions=[
        #{'trigger': 'advance', 'source': 'user', 'dest': 'input_gender', 'conditions': 'is_going_to_input_gender'},
        {'trigger': 'advance', 'source': 'user', 'dest': 'main', 'conditions': 'is_going_to_main'},
        {'trigger': 'advance', 'source': 'happy', 'dest': 'main', 'conditions': 'is_going_to_main'},
        {'trigger': 'advance', 'source': 'EMO', 'dest': 'main', 'conditions': 'is_going_to_main'},
        {'trigger': 'advance', 'source': 'main', 'dest': 'chooseEmo', 'conditions': 'is_going_to_chooseEmo'},
        {'trigger': 'advance', 'source': 'chooseEmo', 'dest': 'happy', 'conditions': 'is_going_to_happy'},
        {'trigger': 'advance', 'source': 'chooseEmo', 'dest': 'EMO', 'conditions': 'is_going_to_EMO'},
        {'trigger': 'advance', 'source': 'main', 'dest': 'chooseTime', 'conditions': 'is_going_to_chooseTime'},
        {'trigger': 'advance', 'source': 'chooseTime', 'dest': 'morning', 'conditions': 'is_going_to_morning'},
        {'trigger': 'advance', 'source': 'morning', 'dest': 'main', 'conditions': 'is_going_to_main'},
        {'trigger': 'advance', 'source': 'chooseTime', 'dest': 'afternoon', 'conditions': 'is_going_to_afternoon'},
        {'trigger': 'advance', 'source': 'afternoon', 'dest': 'main', 'conditions': 'is_going_to_main'},
        {'trigger': 'advance', 'source': 'chooseTime', 'dest': 'night', 'conditions': 'is_going_to_night'},
        {'trigger': 'advance', 'source': 'night', 'dest': 'main', 'conditions': 'is_going_to_main'},
        {'trigger': 'advance', 'source': 'main', 'dest': 'reject1', 'conditions': 'is_going_to_reject1'},
        {'trigger': 'advance', 'source': 'reject1', 'dest': 'main', 'conditions': 'is_going_to_main'},
        {'trigger': 'advance', 'source': 'reject1', 'dest': 'reject2', 'conditions': 'is_going_to_reject2'},
        {'trigger': 'advance', 'source': 'reject2', 'dest': 'main', 'conditions': 'is_going_to_main'},
        #{'trigger': 'advance', 'source': 'user', 'dest': 'choose_emo', 'conditions': 'is_going_choose_emo'},
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            #send_text_message(event.reply_token, "Not Entering any State")
            if machine.state == 'confess':
                send_text_message(event.reply_token, '宣瑋 有件事想認真問你🥺')
                send_text_message(event.reply_token, '我們再一起好不好~')
                send_text_message(event.reply_token, '🥺')

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

show_fsm()

if __name__ == "__main__":
    globals.initialize()
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    #model.get_graph().draw('fsm.png', prog='dot')
    #show_fsm()

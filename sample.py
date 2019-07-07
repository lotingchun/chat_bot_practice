# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 23:19:09 2019

@author: user
"""

from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# 使用heroku的environment variables
line_bot_api = LineBotApi(os.environ['sKPgfSmhQKvcGedV82T6rKwZoNi3F7VeIrRREztQ+4NUcOdLnZbEJ+WsACgqgFOImeKgQXRqdb4feAod4CsA0kIp1jqfYivp3im0XA8oCdHebzUIn704Lykb4r5qbuOEYzZELCEo8He7dw/xqNCjsAdB04t89/1O/w1cDnyilFU='])
handler = WebhookHandler(os.environ['2ed1665107445c1f606a0193a501cc51'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應使用者輸入的話
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Setting host='0.0.0.0' will make Flask available from the network
    app.run(host='0.0.0.0', port=port)
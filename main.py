#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re, os

import telebot
from flask import Flask, request
from pyngrok import ngrok

from core.function import *
from core.token import bot


app = Flask(__name__)
app.secret_key = "super secret key"

def is_link(message):
    try:
        if message.entities[0].type=="url":
            try:
                re.findall(r"http[s]+://[\w\W.]*.com/[\w\W\d\s]+", message.text)[0]
                return True
            except Exception:
                return False
    except Exception:
        return False

@bot.message_handler(commands=["start", "help", "version"])
def default(message):
    funcs = {
        "/start": start,
        "/help": usage,
        "/version": version,
    }
    funcs[message.text](message)


@bot.message_handler(func=lambda message: is_link(message) is True)
def send_video(message):
    download_video(message)


@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method=="POST":
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode("utf-8"))])
        return 'message', 200
    else:
        bot.remove_webhook()
        http_tunnel = ngrok.connect(5000)
        https_tunnel = "https:"+http_tunnel.public_url.split(":")[1]
        bot.set_webhook(url=https_tunnel)
        return "webhook", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
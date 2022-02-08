#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re, os

import telebot
from flask import Flask, request

from core.function import *
from core.token import bot, TOKEN

HEROKU_API = "https://grtiktok.herokuapp.com/"+TOKEN
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


@app.route("/"+TOKEN, methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode("utf-8"))])
    return '!', 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=HEROKU_API)
    return "!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))))
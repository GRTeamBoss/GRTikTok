#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re, os

from flask import Flask
from telebot.types import Update

from .function import *
from .token import TOKEN, bot

APP_URL = "https://grtiktok.herokuapp.com/"+TOKEN
app = Flask(__name__)

PORT = int(os.environ.get('PORT', 5000))


def is_link(update):
    try:
        if update.message.entities[0].type=="url":
            try:
                re.findall(r"http[s]+://[\w\W.]*.com/[\w\W\d\s]+", update.message.text)[0]
                return True
            except Exception:
                return False
    except Exception:
        return False


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
def get_update(request):
    json_string = request.get_data().decode("utf-8")
    update = Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


@app.route("/")
def webhook(request):
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
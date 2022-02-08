#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re, os
import logging

import telebot
from flask import Flask, request
from telebot.types import Update

from core.function import *
from core.token import bot, TOKEN


app = Flask(__name__)
app.secret_key = "super secret key"
APP_URL = "https://grtiktok.herokuapp.com/"+TOKEN

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
    json_string = request.get_data().decode("utf-8")
    update = Update.de_json(json_string)
    bot.process_new_updates([update])
    return "<h1>Work</h1>", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return "<h1>Webhook</h1>", 200
if __name__ == "__main__":
    if "Heroku" in list(os.environ.keys()):
        PORT = int(os.environ.get('PORT', 5000))
        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)
        app.run(host="0.0.0.0", port=PORT)
    else:
        bot.remove_webhook()
        bot.polling(non_stop=True)
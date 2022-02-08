#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re, os, logging, time

import telebot
import flask
from flask import Flask, request

from core.function import *
from core.token import bot, TOKEN


app = Flask(__name__)
app.secret_key = "super secret key"


__webhook_host = '18.192.121.96'
__webhook_port = 8443
__webhook_listen = '0.0.0.0'

__webhook_cert = ''
__webhook_priv = ''

__webhook_base = f'https://{__webhook_host}:{__webhook_port}'
__webhook_path = f'/{TOKEN}/'

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

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


@app.route("/", methods=["GET", "HEAD"])
def index():
    return ''


@app.route(__webhook_path, methods=["POST"])
def webhook():
    if request.headers.get('content-type') == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "<h1>Work</h1>"
    else:
        flask.abort(403)


bot.remove_webhook()

time.sleep(.5)
bot.set_webhook(url=__webhook_base+__webhook_path, certificate=open(__webhook_cert, "r"))

app.run(host=__webhook_listen, port=__webhook_port, ssl_context=(__webhook_cert, __webhook_priv), debug=True)
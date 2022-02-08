#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

import cherrypy

from core.function import *
from core.token import *


WEBHOOK_HOST = "18.192.121.96"
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = "0.0.0.0"
WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f"/{TOKEN}/"


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = bot.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


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


@bot.message_handler(commands=['start', 'help', 'version'])
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

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, "r"))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {"/": {}})
#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re, os

import logging
import cherrypy
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater

from core.function import *


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = "5293683737:AAFDZVtnkCaqoBhwKzco6jZllFInith3Dy0"

PORT = int(os.environ.get('PORT', 5000))


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = Update.de_json(json_string)
            Update([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


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


def default(update: Update, content: CallbackContext):
    funcs = {
        "/start": start,
        "/help": usage,
        "/version": version,
    }
    funcs[update.message.text](update, content)


def send_video(update, content):
    status = is_link(update)
    if status is True:
        download_video(update, content)
    else:
        content.bot.send_message(update.effective_chat.id, "Invalid URI!")


def error(update, content):
    logger.warning('Update "%s" caused error "%s"', update, content.error)


def main():

    bot = Updater(TOKEN, use_context=True)

    dispatcher = bot.dispatcher
    start_handler = CommandHandler('start', default, run_async=True)
    usage_handler = CommandHandler('help', default, run_async=True)
    version_handler = CommandHandler('version', default, run_async=True)
    video_handler = MessageHandler(Filters.text, send_video, run_async=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(usage_handler)
    dispatcher.add_handler(version_handler)
    dispatcher.add_handler(video_handler)
    dispatcher.add_error_handler(error)

    bot.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    bot.bot.set_webhook('https://rocky-shore-11854.herokuapp.com/'+TOKEN)
    bot.idle()


if __name__ == "__main__":
    main()
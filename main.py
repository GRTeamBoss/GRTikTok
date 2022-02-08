#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from telegram import Update

from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, run_async


from core.function import *
from core.token import bot


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
    }
    funcs[update.message.text](update, content)


def send_video(update: Update, content: CallbackContext):
    status = is_link(update)
    if status is True:
        download_video(update, content)
    else:
        bot.send_message(update.effective_chat.id, "Invalid URI!")

dispatcher = bot.dispatcher
start_handler = CommandHandler('start', default, run_async=True)
usage_handler = CommandHandler('help', default, run_async=True)
video_handler = MessageHandler(Filters.text & (~Filters.command), send_video, run_async=True)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(usage_handler)
dispatcher.add_handler(video_handler)

bot.start_polling()
bot.idle()
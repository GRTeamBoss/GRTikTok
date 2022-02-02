#!/usr/bin/env python
#-*- coding:utf-8 -*-

from core.filter import *
from core.function import *
from core.token import bot

@bot.message_handler(commands=["start", "help"])
def default(message):
    funcs = {
        "/start": start,
        "/help": usage,
    }
    funcs[message.text](message)

@bot.message_handler(func=lambda message: is_link(message) is True)
def send_video(message):
    download_video(message)

if __name__=="__main__":
    bot.polling(non_stop=True)

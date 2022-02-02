import requests

from core.token import bot


def start(message) -> None:
    bot.send_message(chat_id=message.chat.id, text="Welcome! I am GRTikTok bot for download video from TT and other services")


def usage(message) -> None:
    info = "This bot might download TT videos, but you will wait minimum 20 second for TT video with 10 second freequency\nFor download just send URI from TT video"
    bot.send_message(chat_id=message.chat.id, text=info)


def download_video(message) -> None:
    __file = requests.get(message.text)
    if __file.status_code == 200:
        bot.send_video(message.chat.id, __file.content)
    else:
        bot.send_message(chat_id=message.chat.id, text=f"Error!\nstatus code: {__file.status_code}")

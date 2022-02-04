import re, subprocess

from TikTokApi import TikTokApi
import requests

from core.token import bot


def start(message) -> None:
    bot.send_message(chat_id=message.chat.id, text="Welcome! I am GRTikTok bot for download video from TT and other services")


def usage(message) -> None:
    info = "This bot might download TT videos, but you will wait minimum 20 second for TT video with 10 second freequency\nFor download just send URI from TT video"
    bot.send_message(chat_id=message.chat.id, text=info)


def download_video(message) -> None:
    bot.send_message(message.chat.id, "Download...")
    try:
        __mobile_link = re.findall(r"https://vm.tiktok.com/[\w\W\s]+", message.text)[0]
    except Exception:
        __usual_link = re.findall(r"https://v[\d]+-webapp.tiktok.com/[\w\W\s\S]+", message.text)[0]
    finally:
        if message.text == __mobile_link:
            __redirect_link = subprocess.check_output(f'curl -s "{__mobile_link}"', stderr=subprocess.STDOUT, shell=True).decode()
            __URI = re.findall(r'="https://m.tiktok.com/[\w\W\s\S]+"', __redirect_link)[0]
            __URL = __URI[2:-1]
            print(__URL)
            __API = TikTokApi().get_video_by_url(video_url=__URL, custom_verifyFP="verify_a70937655d04f49acd1356a7fceb9049")
            print("__API", __API)
            exit()
            __file_link = re.findall(r'src="https://v[\d]+-webapp.tiktok.com/[\w\W\s\S]+"')[0][5:-1]
            __file = requests.get(__file_link)
        elif message.text == __usual_link:
            exit()
            __file = requests.get(message.text)
        else:
            exit()
            bot.send_message(message.chat.id, "Invalid URI!")
    if __file.status_code == 200:
        bot.send_message(message.chat.id, "Success!")
        if len(__file.content)==0:
            bot.send_message(message.chat.id, "Video not finded!")
        else:
            bot.send_video(message.chat.id, __file.content)
    else:
        bot.send_message(chat_id=message.chat.id, text=f"Error!\nstatus code: {__file.status_code}")

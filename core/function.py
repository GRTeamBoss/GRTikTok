import re, time

import requests

from core.token import bot


UA_CHROME = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
UA_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"


def start(message) -> None:
    bot.send_message(chat_id=message.chat.id, text="Welcome! I am GRTikTok bot for download video from TikTok and may be from another services if link from another services not for sharing")


def usage(message) -> None:
    info = "This bot might download TT videos, but you will wait minimum 20 second for TT video with 10 second volume.\nFor download just send URI from TT video or link for share"
    bot.send_message(chat_id=message.chat.id, text=info)


def version(message) -> None:
    info = "(c) GRTikTok\nbeta 0.2.0\nExperimental"
    bot.send_message(chat_id=message.chat.id, text=info)


def download_video_from_share_link(URI: str, message) -> any:
    __page = None
    try:
        __page = requests.get(URI, headers={"User-Agent": UA_CHROME})
    except Exception:
        __page = requests.get(URI, headers={"User-Agent": UA_MOBILE})
    finally:
        if __page is None:
            return False
        elif __page.status_code == 200:
            try:
                __video_tag = re.findall(r'src="https://v[\w\S]+="', __page.text)[0][5:-1]
            except Exception:
                __video_tag = re.findall(r'"downloadAddr":"[\w\S]+="', __page.text)[0][16:-1]
            __URL_decode = "".join("/".join(__video_tag.split("\\u002F")).split("amp;"))
            bot.send_message(chat_id=message.chat.id, text=f"Parsed URI: {__URL_decode}")
            time.sleep(1)
            bot.send_message(chat_id=message.chat.id, text="Video downloading...")
            try:
                __file = requests.get(__URL_decode, headers={"User-Agent": UA_CHROME})
                return __file
            except Exception:
                return False
        else:
            return False


def download_video(message) -> None:
    bot.send_message(message.chat.id, "Download...")
    __mobile_link = ''
    __usual_link = ''
    PC_SHARE = False
    try:
        __mobile_link = re.findall(r"https://vm.tiktok.com/[\w\W\s]+", message.text)[0]
    except Exception:
        try:
            __usual_link = re.findall(r"https://v[\d]+[\w\W\s\S]+", message.text)[0]
        except Exception:
            __usual_link = re.findall(r"https://www.tiktok.com/@[\w\S]+", message.text)[0]
            PC_SHARE = True
    finally:
        time.sleep(1)
        if message.text == __mobile_link:
            __file = download_video_from_share_link(__mobile_link, message)
        elif PC_SHARE is True and message.text == __usual_link:
            __file = download_video_from_share_link(__usual_link, message)
        elif PC_SHARE is False and message.text == __usual_link:
            bot.send_message(chat_id=message.chat.id, text="Video downloading...")
            __file = requests.get(message.text)
        else:
            __file = None
            bot.send_message(message.chat.id, "Invalid URI!")
        if __file is not False and __file is not None:
            if __file.status_code == 200:
                bot.send_message(message.chat.id, "Success!")
                bot.send_video(chat_id=message.chat.id, video=__file.content)
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Error!\nstatus code: {__file.status_code}")
        elif __file is False:
            bot.send_message(chat_id=message.chat.id, text="Error!")
        else:
            pass

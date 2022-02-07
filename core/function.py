import re, time

import requests

from core.token import bot
from core.parse_cookies import ParseCookies


UA_CHROME = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
UA_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
ACCEPT_VIDEO = "*/*"
ACCEPT_LANG_VIDEO = "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
CURL_CONFIG = "-s --http2 --ssl --ssl-allow-beast"

TIKTOK_VIDEO_HEADER = {
    "User-Agent": UA_CHROME,
    "Accept": ACCEPT_VIDEO,
    "Range": "bytes=0-",
    "Referer": "https://www.tiktok.com/",
    "DNT": "1",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": ParseCookies().main(),
}
print(TIKTOK_VIDEO_HEADER["Cookie"])
exit()

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
        __usual_link = re.findall(r"https://v[\d]+[\w\W\s\S]+", message.text)[0]
    finally:
        if message.text == __mobile_link:
            time.sleep(2)
            __page = requests.get(__mobile_link, headers={"User-Agent": UA_MOBILE})
            with open(f"page{message.chat.id}.html", "w", encoding="utf-8") as file:
                file.write(__page.text)
            if __page.status_code == 200:
                __file_content = __page.text
                __video_tag = re.findall(r'src="https://v[\w\S]+="', __file_content)[0]
                __URL = __video_tag[5:-1]
                print("[*]", __URL)
                # __Host = re.findall(r'[^https://][\w\W]+.[\w\W]+.com', __URL)[0]
                # __Path = re.findall(r'/video[\w\W]+', __URL)[0]
                # __file = requests.get(__URL, headers=TIKTOK_VIDEO_HEADER)
                __prompt_requests = "https://api.promptapi.com/scraper?url={url}"
                __prompt_payload = {}
                __prompt_headers = {
                    "apikey": "Qq9d74PXFZ0ESDaV2YKHyRZ7bHdBZMpo",
                }
                __promptapi = requests.request("GET", __prompt_requests.format(url=__URL), headers=__prompt_headers, data=__prompt_payload)
                print("###############")
                print(__promptapi.text)
                print("###############")
                print(__promptapi.content)
                print("###############")
                exit()
            else:
                exit()
                __file = __page
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

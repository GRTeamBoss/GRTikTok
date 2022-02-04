import re


def is_link(message):
    try:
        if message.entities[0].type=="url":
            debug = re.findall(r"http[s]+://[\w\W.]*.com/[\w\W\d\s]+", message.text)[0]
            print("[*] Debug: ", debug)
            return True
        return False
    except Exception:
        return False

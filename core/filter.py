import re


def is_link(message):
    try:
        if message.entities[0].type=="url":
            re.findall(r"http[s]+://[\w\W.]*.com/[\w\W\d]+", message.text)
            return True
        return False
    except Exception:
        return False

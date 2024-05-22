import datetime

def log(text):
    return print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] " + text)
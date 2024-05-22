import datetime

def log(text: str) -> None:
    return print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] " + text)
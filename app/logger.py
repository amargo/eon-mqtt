import time


def log(msg):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{datetime}] {msg}")

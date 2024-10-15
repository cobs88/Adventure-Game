import time
import threading

def type(text, speed=0.01):
    for char in text:
        print(char, end='', flush=True)
        if char in {'.', '?', '!'}:
            time.sleep(speed * 30)
        elif char == ",":
               time.sleep(speed * 15)
        elif char == "\n":
            print()
            if speed == 0.004:
                time.sleep(0)
            else:
                time.sleep(speed * 50)
        time.sleep(speed)

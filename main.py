import cv2
import math
from tkinter import *
import pyautogui
import time
import numpy as np
import matplotlib.pyplot as plt
import win32api, win32con
import keyboard

from utils import RedPixelMatcher

CAPTURE_AREA = [None, None]

QUIT = False # We loop in-game until this is set to True.

def terminate_program():
    global QUIT
    
    QUIT = True
    
    exit(0)

keyboard.add_hotkey('c', terminate_program)

# This defines when two locations are considered as equal.
def callback(event):
    global CAPTURE_AREA

    if CAPTURE_AREA[0] is None:
        CAPTURE_AREA[0] = (event.x, event.y)
        print("Click on the bottom right corner of the area.")
    elif CAPTURE_AREA[1] is None:
        CAPTURE_AREA[1] = (event.x, event.y)

        root.quit()

        root.destroy()

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))

root.bind("<Button-1>", callback)

root.attributes('-alpha', 0.3)

print("Click on the top left corner of the area.")

root.mainloop()

time.sleep(2)

template_matcher = RedPixelMatcher(threshold=200)

while not QUIT:
    img = np.array(pyautogui.screenshot())[CAPTURE_AREA[0][1]:CAPTURE_AREA[1][1], CAPTURE_AREA[0][0]:CAPTURE_AREA[1][0], :]

    match = template_matcher.match_image(img)

    if match:
        (y, x) = match

        win32api.SetCursorPos((CAPTURE_AREA[0][0] + x, CAPTURE_AREA[0][1] + y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    time.sleep(0.25)
import math
import time

import pyautogui
import win32api
import win32con
from PIL import Image
import win32gui
import ctypes
import cv2
import numpy as np
import pydirectinput as pyinput

from loguru import logger

user32 = ctypes.windll.user32

# 定义常量
MOUSEEVENTF_LEFTDOWN = 0x0002  # 鼠标左键按下
MOUSEEVENTF_LEFTUP = 0x0004    # 鼠标左键松开

# 定义结构体
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# 获取鼠标当前位置
def get_cursor_pos():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

# 模拟鼠标点击事件
def mouse_click(x, y):
    user32.SetCursorPos(x, y)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
scale = 1
# 示例：模拟鼠标点击
# x, y = get_cursor_pos()
# print(x,y)
# mouse_click(x, y)
def getX_Y(img, template, threshold = 0.8):
    img = cv2.imread(img)  # 要找的大图
    img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

    template = cv2.imread(template)  # 图中的小图
    template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
    template_size = template.shape[:2]

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_ = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, template_, cv2.TM_CCOEFF_NORMED)

    # res大于70%
    loc = np.where(result >= threshold)
    # 使用灰度图像中的坐标对原始RGB图像进行标记
    point = ()
    for pt in zip(*loc[::-1]):
        # cv2.rectangle(img, pt, (pt[0] + template_size[1], pt[1] + + template_size[0]), (7, 249, 151), 2)
        point = pt
    if point == ():
        return None
    # print(point)
    # cv2.imshow("img", template_)
    # cv2.waitKey()
    return [point[0], point[1]]
    # return img, point[0] + template_size[1] / 2, point[1]


    # img, x_, y_ = search_returnPoint(img, template, template_size)
    return [int(point[0] + template_size[1] / 2), int(point[1])]
def callback(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    # print("Window %s:" % win32gui.GetWindowText(hwnd))
    # print("\tLocation: (%d, %d)" % (x, y))
    # print("\t    Size: (%d, %d)" % (w, h))
    return w, h


def jietu_dnf(x=0, y=0):
    hwnd = win32gui.FindWindow(None, "地下城与勇士：创新世纪")
    time.sleep(0.1)
    win32gui.SetForegroundWindow(hwnd)
    w, h = callback(hwnd)

    win32gui.MoveWindow(hwnd, 0, 0, w, h, True)

    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot.save('./img/dnf.png')

def click(x, y):

    pyinput.moveTo(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)

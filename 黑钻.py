import threading
import time

import pyautogui
import pydirectinput as pyinput
import pynput
import win32gui

import tools


def callback(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    return w, h

def heizuan():
    tools.jietu_dnf()

    a = tools.getX_Y("./img/qidong.png", "./img/dnf.png")
    if a:
        tools.click(a[0], a[1])
        time.sleep(0.1)
        tools.click(449, 351)

    else:
        pyinput.press("esc")
        time.sleep(0.1)
        tools.jietu_dnf()

        a = tools.getX_Y("./img/heizuanji.png", "./img/dnf.png")
        if a:
            tools.click(a[0], a[1])
stop = False

def on_key_press(key):    #当按键按下时记录
    global stop
    print(str(key))
    if str(key)=="'e'":    #如果是e键
        stop = True
        print("F12")
        return False


def start_key_listen():    #用于开始按键的监听
    # 进行监听
    with pynput.keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()
def start_mouse_listen():    #用于开始鼠标的监听
    global stop
    # 进行监听
    while True:
        if stop:
            break
        heizuan()
if __name__ == '__main__':
    key_listen_thread = threading.Thread(target=start_key_listen)
    mouse_listen_thread=threading.Thread(target=start_mouse_listen)
    key_listen_thread.start()
    mouse_listen_thread.start()
    key_listen_thread.join()
    mouse_listen_thread.join()



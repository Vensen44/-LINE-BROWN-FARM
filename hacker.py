# -*- coding: utf-8 -*-
import autopy
import time
import cv2
import pyautogui
import numpy as np
import win32gui

def first_time_run_game():
    '''
    剛開遊戲畫面會在正中央, 移動畫面到特定座標後點選拍賣看板.
    '''
    time.sleep(3)
    autopy.mouse.move(50, 540)  # 移動滑鼠(1920*1080)
    autopy.mouse.toggle(None, True)  # 按下左鍵
    autopy.mouse.smooth_move(1500, 0)  # 平滑移動滑鼠
    autopy.mouse.toggle(None, False)  # 鬆開左鍵
    autopy.mouse.move(1100, 860)
    autopy.mouse.click()


def import_picture():
    '''
    導入特定物品圖片
    '''
    glue = cv2.imread('D:/Desktop/farm/glue.png')
    #board = cv2.imread('D:/Desktop/farm/board.png')
    paper = cv2.imread('D:/Desktop/farm/paper.png')
    ruler = cv2.imread('D:/Desktop/farm/ruler.png')
    nail = cv2.imread('D:/Desktop/farm/nail.png')
    axe = cv2.imread('D:/Desktop/farm/Axe.png')
    hoe = cv2.imread('D:/Desktop/farm/hoe.png')
    flag = cv2.imread('D:/Desktop/farm/flag.png')
    metal = cv2.imread('D:/Desktop/farm/metal.png')
    concrete = cv2.imread('D:/Desktop/farm/concrete.png')
    check = cv2.imread('D:/Desktop/farm/check.png')
    paint = cv2.imread('D:/Desktop/farm/paint.png')
    return glue, paper, ruler, axe, hoe, flag, nail, metal, concrete, paint, check


def find_image(item_in):
    '''
    擷取螢幕,找出特定物品的位置並回傳座標.

    TM_SQDIFF 平方差匹配法:該方法採用平方差來進行匹配；最好的匹配值為0；匹配越差，匹配值越大.
    TM_CCORR 相關匹配法:該方法採用乘法操作;數值越大表明匹配程度越好.
    TM_CCOEFF 相關係數匹配法:1表示完美的匹配；-1表示最差的匹配.
    TM_SQDIFF_NORMED 歸一化平方差匹配法.
    TM_CCORR_NORMED 歸一化相關匹配法.
    TM_CCOEFF_NORMED 歸一化相關係數匹配法.
    '''
    screen_shot = pyautogui.screenshot(region=[0, 0, 1919, 1079])  # x,y,w,h
    screen_shot = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2BGR)
    cv2.imwrite('D:/Desktop/farm/screenshot.png', screen_shot)
    screen = cv2.imread('D:/Desktop/farm/screenshot.png')
    res = cv2.matchTemplate(screen, item_in, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= 0.98:
        return max_loc
    else:
        return None


def get_item_home(item):
    '''
    尋找所需物品(item),找到就點擊前往,這頁沒找到就往後翻,若都沒有就點擊返回鈕
    '''
    for slide in range(0, 6):
        if slide == 1:
            time.sleep(0.5)
        position = find_image(item)
        if position:
            autopy.mouse.move(position[0], position[1])
            autopy.mouse.click()  # 單擊
            return True  # 若找到了,就不用再往後找
        else:
            # 若沒找到,往後滑
            autopy.mouse.move(50, 540)
            autopy.mouse.toggle(None, True)  # 按下左鍵
            autopy.mouse.smooth_move(25, 540)  # 平滑移動滑鼠
            autopy.mouse.toggle(None, False)  # 鬆開左鍵
            time.sleep(0.01)
    autopy.mouse.move(75, 100)  # 移動滑鼠到返回鈕
    autopy.mouse.click()  # 單擊
    return False


def get_item_other_home(item):
    '''
    尋找所需物品(item),找到後買下,之後出去頁面繼續等下次更新看板
    '''
    position = find_image(item)
    for slide in range(0, 3):
        if position:
            autopy.mouse.move(position[0], position[1])
            autopy.mouse.click()  # 單擊
            autopy.mouse.move(75, 100)  # 移動滑鼠到返回鈕
            autopy.mouse.click()  # 單擊
            break  # 若找到了,就不用再往後找
        else:
            # 若沒找到,往後滑
            autopy.mouse.move(860, 200)
            autopy.mouse.toggle(None, True)  # 按下左鍵
            autopy.mouse.smooth_move(50, 200)  # 平滑移動滑鼠
            autopy.mouse.toggle(None, False)  # 鬆開左鍵
    autopy.mouse.move(75, 100)  # 移動滑鼠到返回鈕
    autopy.mouse.click()  # 單擊


def wait_read(item):
    '''
    等待讀取畫面
    '''
    while(1):
        screen_shot = pyautogui.screenshot(region=[0, 0, 1919, 1079])  # x,y,w,h
        screen_shot = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2BGR)
        cv2.imwrite('D:/Desktop/farm/screenshot.png', screen_shot)
        screen = cv2.imread('D:/Desktop/farm/screenshot.png')
        res = cv2.matchTemplate(screen, item, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val >= 0.98:
            break




item_get, item_get2, item_get3, item_get4, item_get5, item_get6, item_get7, item_get8, item_get9, item_get10, item_check = import_picture()
# 1-glue, 2-paper, 3-ruler, 4-Axe, 5-hoe, 6-flag, 7-nail, 8-metal, 9-concrete, 10-paint
wanted_item = item_get10  # 想要找的物品
first_time_run_game()  # 移動後點入看板
time.sleep(3)  # 點入看板後等待讀取


while(1):
    # 只做第一回尋找,其他回是在別人家的看板找的
    get_or_not = get_item_home(wanted_item)
    if get_or_not:
        wait_read(item_check)
        get_item_other_home(wanted_item)
        break
    else:
        time.sleep(180)  # 等看板更新(三分鐘)
        autopy.mouse.move(1100, 860)  # 移動滑鼠到看板
        autopy.mouse.click()  # 點擊看板
        time.sleep(3)  # 點入看板後等待讀取


autopy.mouse.move(1300, 860)  # 移動滑鼠到看板
autopy.mouse.click()  # 點擊看板
time.sleep(3)  # 點入看板後等待讀取
while(1):
    # 在別人家裡點擊看板尋找
    get_or_not = get_item_home(wanted_item)
    if get_or_not:
        wait_read(item_check)
        get_item_other_home(wanted_item)
        autopy.mouse.move(1300, 860)  # 移動滑鼠到看板
        time.sleep(180)  # 等看板更新(三分鐘)
        autopy.mouse.click()  # 點擊看板
        time.sleep(3)  # 點入看板後等待讀取
    else:
        autopy.mouse.move(1300, 860)  # 移動滑鼠到看板
        time.sleep(180)  # 等看板更新(三分鐘)
        autopy.mouse.click()  # 點擊看板
        time.sleep(3)  # 點入看板後等待讀取

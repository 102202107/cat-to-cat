from tkinter import font
import pgzrun  
import pygame  
import random  
from pgzero.builtins import Actor  
from pgzero.builtins import Rect  
import time
  
# 定义游戏相关属性  
TITLE = '喵了个咪'  
WIDTH = 700  
HEIGHT = 740  
  
# 自定义游戏常量  
T_WIDTH = 60  
T_HEIGHT = 66  
  
# 下方牌堆的位置  
DOCK = Rect((0, 670), (T_WIDTH * 7, T_HEIGHT))  
  
# 上方的所有牌  
tiles = []  
# 牌堆里的牌  
docks = []  
  
# 初始化牌组，12*12张牌随机打乱  
ts = list(range(1, 13)) * 12  
random.shuffle(ts)  
n = 0  
for k in range(7):  # 7层  
    for i in range(7 - k):  # 每层减1行  
        for j in range(7 - k):  
            t = ts[n]  
            n += 1  
            tile = Actor(f'tile{t}')  
            tile.pos = 120 + (k * 0.5 + j) * tile.width, 100 + (k * 0.5 + i) * tile.height * 0.9  
            tile.tag = t  
            tile.layer = k  
            tile.status = 1 if k == 6 else 0  
            tiles.append(tile)  
for i in range(4):  # 剩余的4张牌放下面（为了凑整能通关）  
    t = ts[n]  
    n += 1  
    tile = Actor(f'tile{t}')  
    tile.pos = 210 + i * tile.width, 516  
    tile.tag = t  
    tile.layer = 0  
    tile.status = 1  
    tiles.append(tile)  
  
# 初始化倒计时  
countdown_time = 180  
start_time = None  # 初始化为None，在游戏开始时设置  
  
# 初始画面显示标志  
show_start_screen = True  
  
# 游戏帧绘制函数  
def draw():  
    screen.clear()  
    if show_start_screen:  
        screen.blit('begin', (0, 0))  
    else:  
        screen.blit('back', (0, 0))  
        for tile in tiles:  
            tile.draw()  
            if tile.status == 0:  
                screen.blit('mask', tile.topleft)  
        for i, tile in enumerate(docks):  
            tile.left = DOCK.x + i * T_WIDTH  
            tile.top = DOCK.y  
            tile.draw()  
  
        # 绘制倒计时和其他游戏元素（如果游戏已开始）  
        if not show_start_screen:  
            elapsed_time = time.time() - start_time  
            remaining_time = max(0, countdown_time - int(elapsed_time))  
            font = pygame.font.SysFont(None, 40)  
            text_surface = font.render(f'Time left: {remaining_time}s', True, (255, 0, 0))  
            screen.blit(text_surface, (250, 10))  
  
            # 检查游戏结束条件  
            if len(docks) >= 7:  
                screen.blit('end', (0, 0))  
            if len(tiles) == 0:  
                screen.blit('win', (0, 0))  
  
# 鼠标点击响应  
def on_mouse_down(pos):  
    global show_start_screen, start_time, docks  
    if show_start_screen:  
        show_start_screen = False  
        start_time = time.time()  # 游戏开始计时  
        return  
  
    if len(docks) >= 7 or len(tiles) == 0:  
        return  
  
    for tile in reversed(tiles):  
        if tile.status == 1 and tile.collidepoint(pos):  
            tile.status = 2  
            tiles.remove(tile)  
            diff = [t for t in docks if t.tag != tile.tag]  
            if len(docks) - len(diff) < 2:  
                docks.append(tile)  
            else:  
                docks = diff  
            for down in tiles:  
                if down.layer == tile.layer - 1 and down.colliderect(tile):  
                    for up in tiles:  
                        if up.layer == down.layer + 1 and up.colliderect(down):  
                            break  
                    else:  
                        down.status = 1  
  
# 初始化音乐（如果需要）  
music.play('bgm')  # 注意：这里需要确保'bgm'文件已加载并可用  
  
pgzrun.go()
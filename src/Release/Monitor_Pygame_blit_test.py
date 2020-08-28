# coding: utf-8

import os
import time
from itertools import cycle

import cv2
import pygame
from pygame.locals import *

import numpy as np
import math
from scipy.interpolate import griddata
from colour import Color

import Sensor

########################################################
# デフォルト(iniファイルからの読み込みで上書き)
# カメラ表示の幅
CAMERA_WIDTH = 640
# カメラ表示の高さ
CAMERA_HEIGHT = 480
# サーモ表示の幅
THERMO_WIDTH = 160
# サーモ表示の高さ
THERMO_HEIGHT = 160

# センサ設定    
#low range of the sensor (this will be blue on the screen)
THERMO_MINTEMP = 26
#high range of the sensor (this will be red on the screen)
THERMO_MAXTEMP = 37.5
#how many color values we can have
THERMO_COLORDEPTH = 1024

#####################################################################################################
class MySprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        # デフォルトグループをセット
        pygame.sprite.Sprite.__init__(self, self.containers)

#####################################################################################################
# iniファイルのパラメータを設定
def set_monitor_parameter(camera_width, camera_height, thermo_width, thermo_height, thermo_mintemp, thermo_maxtemp, thermo_colordepth):

    global CAMERA_WIDTH
    CAMERA_WIDTH = camera_width

    global CAMERA_HEIGHT
    CAMERA_HEIGHT = camera_height

    global THERMO_WIDTH
    THERMO_WIDTH = thermo_width

    global THERMO_HEIGHT
    THERMO_HEIGHT = thermo_height

    global THERMO_MINTEMP
    THERMO_MINTEMP = thermo_mintemp

    global THERMO_MAXTEMP
    THERMO_MAXTEMP = thermo_maxtemp

    global THERMO_COLORDEPTH
    THERMO_COLORDEPTH = thermo_colordepth

#####################################################################################################
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

#####################################################################################################
def mapping(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#####################################################################################################
# OpenCVの画像をPygame用に変換
def convert_opencv_img_to_pygame(opencv_image):

    # OpenCVはBGR、PygameはRGBなので変換する必要がある
    opencv_image = opencv_image[:,:,::-1]
    # OpenCVは(高さ, 幅, 色数)、Pygameは(幅, 高さ)なのでこれも変換する
    shape = opencv_image.shape[1::-1]
    pygame_image = pygame.image.frombuffer(opencv_image.tostring(), shape, 'RGB')

    return pygame_image

#####################################################################################################
# 初期化画面を表示
def display_initialize_cheking():
    print("display_initialize_cheking")

    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)
    lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
    lcd.fill((0,0,0))                   # 黒

    # 文字表示 #############################
    pygame.font.init()
    TextColor = (255, 255, 255)         # 白
    Message = "暫くお待ちください"

    font = pygame.font.SysFont("notosansmonocjkjp", 25, bold=True, italic=False)
    text = font.render(Message, True, TextColor)
    lcd.blit(text, (200,200))
    # 文字表示 #############################

    # 画面を更新
    pygame.display.update()

#####################################################################################################
# 初期化画面(接続確認の結果)を表示
def display_initialize_checked(camera_connect_check_result, sensor_connect_check_result):
    print("display_initialize_checked")

    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)
    lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
    lcd.fill((0,0,0))                   # 黒

    # 文字表示 #############################
    pygame.font.init()
    TextColor = (255, 255, 255)         # 白

    if(camera_connect_check_result):
        camera_text = " カメラの接続に成功しました"
    else:
        camera_text = " カメラの接続に失敗しました"

    if(sensor_connect_check_result):
        sensor_text = " センサの接続に成功しました"
    else:
        sensor_text = " センサの接続に失敗しました"

    font1 = pygame.font.SysFont("notosansmonocjkjp", 20, bold=True, italic=False)
    text1 = font1.render(camera_text, True, TextColor)
    font2 = pygame.font.SysFont("notosansmonocjkjp", 20, bold=True, italic=False)
    text2 = font2.render(sensor_text, True, TextColor)

    lcd.blit(text1, (180,200))
    lcd.blit(text2, (180,230))
    # 文字表示 #############################
    
    # 画面を更新
    pygame.display.update()

#####################################################################################################
# 電源OFF画面を表示
def display_turnoff():
    print("display_turnoff")

    # 全画面設定フラグ
    fullscreen_flag = True

    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)
    lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
    
    # スプライトグループを作成してスプライトクラスに割り当て
    group = pygame.sprite.RenderUpdates()
    MySprite.containers = group

    lcd.fill((0,0,0))                   # 黒
    pygame.display.update()

    while True:
        # 文字表示 #############################
        pygame.font.init()
        TextColor = (255, 255, 255)         # 白

        reboot_text = "電源OFF後、接続を確認して再度電源ONしてください"
                
        font3 = pygame.font.SysFont("notosansmonocjkjp", 20, bold=False, italic=False)
        text3 = font3.render(reboot_text, True, TextColor)

        lcd.blit(text3, (80,200))
        # 文字表示 #############################

        # 画面を更新
        pygame.display.update()

        # 通常画面と全画面表示の切り替え
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_F2:
                # F2キーで通常画面と全画面の切り替え
                fullscreen_flag = not fullscreen_flag
                print("fullscreen_flag: " + str(fullscreen_flag))

                if fullscreen_flag:
                    # 全画面
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.FULLSCREEN)
                else:
                    # 通常画面
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.RESIZABLE)

#####################################################################################################
# カメラ画像とサーモグラフィーを表示
def display_camera_thermography_faceframe(frame, bicubic, lcd, colors, displayPixelHeight, displayPixelWidth):

    print("display_camera_thermography_faceframe")
    # カメラ画像を左右反転
    frame_flip_lr = cv2.flip(frame, 1)

    # OpenCVの画像をPygame用に変換
    pygame_image = convert_opencv_img_to_pygame(frame_flip_lr)

    # カメラ表示
    lcd.blit(pygame_image, (0, 0))

    # サーモ表示 ##########################################################################
    thermo_offset_x = 0
    thermo_offset_y = CAMERA_HEIGHT - THERMO_HEIGHT

    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, THERMO_COLORDEPTH- 1)], \
                                (thermo_offset_x + displayPixelHeight * ix, thermo_offset_y + displayPixelWidth * jx, \
                                displayPixelHeight, displayPixelWidth))
    # サーモ表示 ##########################################################################

    # 顔枠を表示
    pygame.draw.rect(lcd, (0, 0, 255), (220, 90, 200, 300), 3)

#####################################################################################################
def display_wait_detect_finish(cap):

    print ("### Monitor_Func ###")

    # 全画面設定フラグ
    fullscreen_flag = True

    # センサ設定 ############################################################################
    os.putenv('SDL_FBDEV', '/dev/fb1')

    points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
    grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

    #the list of colors we can choose from
    blue = Color("indigo")
    colors = list(blue.range_to(Color("red"), THERMO_COLORDEPTH))

    #create the array of colors
    colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
    # センサ設定 ############################################################################

    # センサからの32x32配列データを160x160で表示する
    displayPixelWidth = THERMO_WIDTH / 32
    displayPixelHeight = THERMO_HEIGHT / 32

    # Pygame設定 ############################################################################
    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)
    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.FULLSCREEN)

    clock = pygame.time.Clock()

    BLINK_EVENT = pygame.USEREVENT + 0

    # イベント(文字の点滅)の周期を設定
    pygame.time.set_timer(BLINK_EVENT, 500)     # ms

    # スプライトグループを作成してスプライトクラスに割り当て
    group = pygame.sprite.RenderUpdates()
    MySprite.containers = group

    lcd.fill((255,0,0))

    pygame.display.update()
    pygame.mouse.set_visible(False)

    lcd.fill((0,0,0))
    pygame.display.update()
    # Pygame設定 ############################################################################

    while True:
        # カメラ画像取得(1コマ分のキャプチャ画像データを読み込む)
        _, frame = cap.read()
        if(frame is None):
            continue

        # センサデータ更新
        Sensor.measurement_temperature_and_status()

        # センサから配列データを取得
        pixels = Sensor.get_temperature_array()
        print (pixels)
        pixels = [mapping(p, THERMO_MINTEMP, THERMO_MAXTEMP, 0, THERMO_COLORDEPTH - 1) for p in pixels]
	
        # bicubic補間
        bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
	
        # センサから状態を取得
        state = Sensor.get_state()

        if(state == "WAIT"):        # 待機中
            # カメラ画像とサーモグラフィーを表示
            display_camera_thermography_faceframe(frame, bicubic, lcd, colors, displayPixelHeight, displayPixelWidth)
            
            # スプライトグループを更新
            group.update()
            # スプライトグループを描画
            group.draw(lcd)
            # 画面を更新
            pygame.display.update()

        if(state == "DETECT"):      # 測定中
            # カメラ画像とサーモグラフィーを表示
            display_camera_thermography_faceframe(frame, bicubic, lcd, colors, displayPixelHeight, displayPixelWidth)
            
            # 文字を表示(文字表示) ################
            pygame.font.init()
            background_color = (0, 0, 0)
            TextColor = (255, 255, 255)         # 白
            Message = "測定中"

            font = pygame.font.SysFont("notosansmonocjkjp", 20, bold=True, italic=False)
            on_text = font.render(Message, True, TextColor, background_color)
            blink_rect = on_text.get_rect()

            off_text = pygame.Surface(blink_rect.size)
            blink_surfaces = cycle([on_text, off_text])
            blink_surface = next(blink_surfaces)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == BLINK_EVENT:
                    print("### BLINK_EVENT ###")
                    blink_surface = next(blink_surfaces)

            lcd.blit(blink_surface, (0,280))
            # 文字表示 #############################

            # スプライトグループを更新
            group.update()
            # スプライトグループを描画
            group.draw(lcd)
            # 画面を更新
            pygame.display.update()

            clock.tick(60)

        if(state == "FINISH"):       # 測定終了
            # カメラ画像とサーモグラフィーを表示
            display_camera_thermography_faceframe(frame, bicubic, lcd, colors, displayPixelHeight, displayPixelWidth)
            
            # 文字表示(最高温度、測定結果) ##########
            pygame.font.init()
            # 背景色
            background_color = (0, 0, 0)        # 黒
            # 最高温度
            MaxTempStr = str(Sensor.get_max_temperature()) + "℃"
            # 発熱判定によって、表示するテキストの色とメッセージを変える
            if(Sensor.get_isfever() == True):
                TextColor = (255, 0, 0)         # 赤
                DetectResult = "正確な検温を行ってください。"
            else:
                TextColor = (0, 255, 0)         # 緑
                DetectResult = "平熱です。"

            font1 = pygame.font.SysFont("notosansmonocjkjp", 20, bold=True, italic=False)
            text1 = font1.render(MaxTempStr, True, TextColor, background_color)

            font2 = pygame.font.SysFont("notosansmonocjkjp", 15, bold=True, italic=False)
            text2 = font2.render(DetectResult, True, TextColor, background_color)

            lcd.blit(text1, (0,250))
            lcd.blit(text2, (0,290))
            # 文字表示 #############################

           # スプライトグループを更新
            group.update()
            # スプライトグループを描画
            group.draw(lcd)
            # 画面を更新
            pygame.display.update()

        #############################################################################
        # 通常画面と全画面表示の切り替え
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_F2:
                # F2キーで通常画面と全画面の切り替え
                fullscreen_flag = not fullscreen_flag
                print("fullscreen_flag: " + str(fullscreen_flag))

                if fullscreen_flag:
                    # 全画面
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.FULLSCREEN)
                else:
                    # 通常画面
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.RESIZABLE)
        #############################################################################



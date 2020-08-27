# coding: utf-8

import cv2
#print(cv2.__version__)
#from PIL import ImageFont, ImageDraw, Image
import numpy as np
#import matplotlib.pyplot as plt

# センサ接続に必要
import adafruit_amg88xx

import time
import itertools

import Sensor

from pygame.locals import *
from itertools import cycle

######################  Pygameお試し ############################
from Adafruit_AMG88xx import Adafruit_AMG88xx
import pygame
import os
import math
from scipy.interpolate import griddata
from colour import Color

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def mapping(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def convert_opencv_img_to_pygame(opencv_image):
    """
    OpenCVの画像をPygame用に変換.

    see https://blanktar.jp/blog/2016/01/pygame-draw-opencv-image.html
    """
    opencv_image = opencv_image[:,:,::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
    shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
    pygame_image = pygame.image.frombuffer(opencv_image.tostring(), shape, 'RGB')

    return pygame_image

class MySprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        # デフォルトグループをセット
        pygame.sprite.Sprite.__init__(self, self.containers)

######################  Pygameお試し ############################

#####################################################################################################
def display_initialize_cheking():
    print("display_initialize_cheking")

    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, 640, 480)
    lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
    lcd.fill((0,0,0))                   # 黒

    # 文字を表示(文字表示) ################
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
def display_initialize_checked(camera_connect_check_result, sensor_connect_check_result):
    print("display_initialize_checked")

    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, 640, 480)
    lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
    lcd.fill((0,0,0))                   # 黒

    # 文字を表示(文字表示) ################
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
    
    # 画面を更新
    pygame.display.update()

#####################################################################################################
def display_turnoff():
    print("display_turnoff")

    # 全画面設定フラグ
    fullscreen_flag = True

    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, 640, 480)
    lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
    
    # スプライトグループを作成してスプライトクラスに割り当て
    group = pygame.sprite.RenderUpdates()
    MySprite.containers = group

    lcd.fill((0,0,0))                   # 黒
    pygame.display.update()

    while True:

        # 文字を表示(文字表示) ################
        pygame.font.init()
        TextColor = (255, 255, 255)         # 白

        reboot_text = "電源OFF後、接続を確認して再度電源ONしてください"
                
        #font3 = pygame.font.SysFont("notosansmonocjkjp", 20, bold=True, italic=False)
        font3 = pygame.font.SysFont("notosansmonocjkjp", 20, bold=False, italic=False)
        text3 = font3.render(reboot_text, True, TextColor)

        #lcd.blit(text3, (80,270))
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
                    print("フルスクリーン")
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.FULLSCREEN)
                else:
                    print("通常スクリーン")
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.RESIZABLE)

#####################################################################################################
# カメラ画像とサーモグラフィーを表示
# ToDo：引数整理
def display_camera_thermography_faceframe(frame, bicubic, lcd, colors, COLORDEPTH, displayPixelHeight, displayPixelWidth, WIDTH, HEIGHT):

    print("display_camera_thermography_faceframe")
    # カメラ画像を左右反転
    frame_flip_lr = cv2.flip(frame, 1)

    # OpenCVの画像をPygame用に変換
    pygame_image = convert_opencv_img_to_pygame(frame_flip_lr)

    # カメラ表示
    lcd.blit(pygame_image, (0, 0))

    # サーモ表示 ##########################################################################
    thermo_offset_x = 0
    thermo_offset_y = 480 - 160

    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], \
                                (thermo_offset_x + displayPixelHeight * ix, thermo_offset_y + displayPixelWidth * jx, \
                                displayPixelHeight, displayPixelWidth))
    # サーモ表示 ##########################################################################

    # 顔枠を表示
    #pygame.draw.rect(lcd, (0, 0, 255), (220, 140, 200, 200), 3)
    pygame.draw.rect(lcd, (0, 0, 255), (220, 90, 200, 300), 3)

#####################################################################################################
# ToDo：引数整理
#def Monitor_Func(cap, WIDTH, HEIGHT, STATUS):
def Monitor_Func(cap, WIDTH, HEIGHT, max_temp_fix, STATUS, DETECT_TH, sensor_pixels):

    print ("### Monitor_Func ###")
    print ("STATUS:" + STATUS)

    # 全画面設定フラグ
    fullscreen_flag = True

    ######################  Pygameお試し ############################
    # センサ初期化、サイズ設定など
    #low range of the sensor (this will be blue on the screen)
    MINTEMP = 26

    #high range of the sensor (this will be red on the screen)
    MAXTEMP = 37.5

    #how many color values we can have
    COLORDEPTH = 1024

    os.putenv('SDL_FBDEV', '/dev/fb1')

    #initialize the sensor
    #sensor = Adafruit_AMG88xx()

    #let the sensor initialize
    time.sleep(.1)

    points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
    grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

    #sensor is an 8x8 grid so lets do a square
    #width = 640
    #height = 480
    
    #the list of colors we can choose from
    blue = Color("indigo")
    colors = list(blue.range_to(Color("red"), COLORDEPTH))

    #create the array of colors
    colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

    # センサからの32x32配列データを160x160で表示する
    displayPixelHeight = 160 / 32
    displayPixelWidth = 160 / 32

    # Pygameを初期化
    pygame.init()

    SCR_RECT = Rect(0, 0, 640, 480)
    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.FULLSCREEN)

    #lcd_rect = lcd.get_rect()
    clock = pygame.time.Clock()

    BLINK_EVENT = pygame.USEREVENT + 0

    #pygame.time.set_timer(BLINK_EVENT, 1000)
    pygame.time.set_timer(BLINK_EVENT, 250)

    # スプライトグループを作成してスプライトクラスに割り当て
    group = pygame.sprite.RenderUpdates()
    MySprite.containers = group

    lcd.fill((255,0,0))

    pygame.display.update()
    pygame.mouse.set_visible(False)

    lcd.fill((0,0,0))
    pygame.display.update()
    ######################  Pygameお試し ############################

    while True:

        # カメラ画像取得
        # 1コマ分のキャプチャ画像データを読み込む
        _, frame = cap.read()
        if(frame is None):
            continue

        # センサデータ更新
        Sensor.measurement_temperature_and_status()

        ######################  Pygameお試し ############################
        #read the pixels
        measure_start_time = time.time()
        pixels = Sensor.get_temperature_array()
        print (pixels)
        elapsed_time = time.time() - measure_start_time
        print ("GetSensorData:{0}".format(elapsed_time) + "[sec]")

        pixels = [mapping(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
	
        #perdorm interpolation
        bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
        #pygame_image_bicubic = pygame.surfarray.make_surface(bicubic)
        #print(pygame_image_bicubic)
	
        state = Sensor.get_state()
        #state = "WAIT"
        #state = "DETECT"
        #state = "FINISH"

        ######################  Pygameお試し ############################

        if(state == "WAIT"):
            # カメラ画像とサーモグラフィーを表示
            display_camera_thermography_faceframe(frame, bicubic, lcd, colors, COLORDEPTH, displayPixelHeight, displayPixelWidth, WIDTH, HEIGHT)
            
            # スプライトグループを更新
            group.update()
            # スプライトグループを描画
            group.draw(lcd)
            # 画面を更新
            pygame.display.update()

        if(state == "DETECT"):
            # カメラ画像とサーモグラフィーを表示
            display_camera_thermography_faceframe(frame, bicubic, lcd, colors, COLORDEPTH, displayPixelHeight, displayPixelWidth, WIDTH, HEIGHT)
            
            # 文字を表示(文字表示) ################
            pygame.font.init()
            background_color = (0, 0, 0)
            TextColor = (255, 255, 255)         # 白
            Message = "測定中"

            font = pygame.font.SysFont("notosansmonocjkjp", 20, bold=True, italic=False)
            #text = font.render(Message, True, TextColor, background_color)
            on_text = font.render(Message, True, TextColor, background_color)
            blink_rect = on_text.get_rect()
            #blink_rect.center = lcd_rect.center

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

        if(state == "FINISH"):
            # カメラ画像とサーモグラフィーを表示
            display_camera_thermography_faceframe(frame, bicubic, lcd, colors, COLORDEPTH, displayPixelHeight, displayPixelWidth, WIDTH, HEIGHT)
            
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
                    print("フルスクリーン")
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.FULLSCREEN)
                else:
                    print("通常スクリーン")
                    pygame.display.quit()
                    pygame.display.init()
                    lcd = pygame.display.set_mode(SCR_RECT.size, pygame.RESIZABLE)
        #############################################################################

        # キュー入力判定
        # "q"でループから抜ける
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    # VideoCaptureオブジェクト破棄
    # USBカメラを閉じる
    #cap.release()
    #cv2.destroyAllWindows()


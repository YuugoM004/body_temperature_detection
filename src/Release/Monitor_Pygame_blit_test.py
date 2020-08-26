# coding: utf-8

import cv2
print(cv2.__version__)
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import matplotlib.pyplot as plt

# センサ接続に必要
import adafruit_amg88xx

import time
import itertools

import Sensor

from pygame.locals import *

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

def Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels):

    # サーモグラフィー表示

    # bicubic補間したデータ
    #measure_start_time = time.time()
    #fig = plt.imshow(sensor_pixels, cmap="inferno", interpolation="bicubic")
    #elapsed_time = time.time() - measure_start_time
    #print ("  imshow:{0}".format(elapsed_time) + "[sec]")

    # plt.colorbar()

    # plt.showだと止まってしまうので、pauseを使用
    # plt.clfしないとカラーバーが多数表示される
    #measure_start_time = time.time()
    #plt.pause(.1)
    #elapsed_time = time.time() - measure_start_time
    #print ("  pause:{0}".format(elapsed_time) + "[sec]")

    #measure_start_time = time.time()
    #plt.clf()
    #elapsed_time = time.time() - measure_start_time
    #print ("  clf:{0}".format(elapsed_time) + "[sec]")

    # カメラ画像を左右反転
    frame_flip_lr = cv2.flip(frame, 1)

    # グレースケール表示
    measure_start_time = time.time()
    resize_width = 160
    resize_height = 160
    frame_flip_lr_resize = cv2.resize(frame_flip_lr,(resize_width, resize_height))
    elapsed_time = time.time() - measure_start_time
    print ("  resize:{0}".format(elapsed_time) + "[sec]")

    measure_start_time = time.time()
    frame_flip_lr_resize_gray = cv2.cvtColor(frame_flip_lr_resize,cv2.COLOR_BGR2GRAY)
    elapsed_time = time.time() - measure_start_time
    print ("  cvtColor:{0}".format(elapsed_time) + "[sec]")

    # グレースケール(2次元配列)をRGB(3次元配列)に変換する
    measure_start_time = time.time()
    frame_flip_lr_resize_gray_array = frame_flip_lr_resize_gray[:, :, None]

    height, width = frame_flip_lr_resize_gray.shape
    x_offset = 0
    y_offset = HEIGHT - resize_height

    frame_flip_lr[y_offset:height + y_offset, x_offset:width + x_offset] = frame_flip_lr_resize_gray_array
    elapsed_time = time.time() - measure_start_time
    print ("  other:{0}".format(elapsed_time) + "[sec]")

    return frame_flip_lr

def Monitor_Func(cap, WIDTH, HEIGHT, max_temp_fix, STATUS, DETECT_TH, sensor_pixels):

    print ("### Monitor_Func ###")
    print ("STATUS:" + STATUS)

    # 全画面設定フラグ
    fullscreen_flag = True

    ######################  Pygameお試し ############################
    # Pygameお試し
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
    width = 640
    height = 480
    
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
    lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)

    # スプライトグループを作成してスプライトクラスに割り当て
    group = pygame.sprite.RenderUpdates()
    MySprite.containers = group

    # 最終的に描画したいサイズでdisplaySurface作成
    #final_display_size_h = 1920
    #final_display_size_v = 1200
    #pygame.display.set_mode((final_display_size_h, final_display_size_v))

    # 動かしたいサイズで別のSurface作成
    #lcd = pygame.Surface((width, height))
    #lcd = pygame.display.set_mode((width, height))

    # 全画面表示
    #lcd = pygame.display.set_mode((0,0))
    #lcd = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #lcd = pygame.display.set_mode((640,480), pygame.FULLSCREEN)

    lcd.fill((255,0,0))

    pygame.display.update()
    pygame.mouse.set_visible(False)

    lcd.fill((0,0,0))
    pygame.display.update()
    ######################  Pygameお試し ############################

    ## 本来はSensor.pyでやる処理だが、デバッグ用にここでセンサのインスタンスを取得
    # センサーの初期化
    #sensor = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x68)
    # センサーの初期化待ち
    #time.sleep(.1)
    ## ここまで

    plt.figure(figsize=(1, 1), dpi=160)

    while True:

        # カメラ画像取得
        # 1コマ分のキャプチャ画像データを読み込む
        _, frame = cap.read()
        if(frame is None):
            continue

        # センサデータ更新
        Sensor.measurement_temperature_and_status()

        ## 本来はSensor.pyでやる処理だが、デバッグ用にここでセンサデータを取得
        # 8x8の表示
        # print (sensor.pixels)

        # 温度データ取得＆最高温度の計算
        #measure_start_time = time.time()
        #sensor_pixels = sensor.pixels
        #max_temp = max(itertools.chain.from_iterable(sensor_pixels))
        #print ("センサ最高温度:" + str(max_temp))
        #elapsed_time = time.time() - measure_start_time
        #print ("GetSensorData & CalcMaxTemp:{0}".format(elapsed_time) + "[sec]")
        ## ここまで

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
        pygame_image_bicubic = pygame.surfarray.make_surface(bicubic)
        print(pygame_image_bicubic)
	
        #draw everything
        #for ix, row in enumerate(bicubic):
        #    for jx, pixel in enumerate(row):
        #        pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
        #
        #pygame.display.update()

        state = Sensor.get_state()

        ######################  Pygameお試し ############################

        if(state == "WAIT"):
            # カメラ画像とサーモグラフィー表示
            #result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels)
            result_frame = frame

            # OpenCVの画像をPygame用に変換
            pygame_image = convert_opencv_img_to_pygame(result_frame)

            # カメラ表示
            lcd.blit(pygame_image, (0, 0))

            # サーモ表示 ##########################################################################
            thermo_offset_x = 0
            thermo_offset_y = 480 - 160

            for ix, row in enumerate(sensor_pixels):
                for jx, pixel in enumerate(row):
                    pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (thermo_offset_x + displayPixelHeight * ix, thermo_offset_y + displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
            # サーモ表示 ##########################################################################

            # 画面を更新
            pygame.display.update()

            # 画像表示
            #cv2.imshow("BodyTemperatureDetection", result_frame)
            # ウインドウ表示位置指定
            #cv2.moveWindow("BodyTemperatureDetection", window_display_pos_x,window_display_pos_y)

        if(state == "DETECT"):
            # カメラ画像とサーモグラフィー表示
            result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels)

            # 測定中を表示
            font_path = "/usr/share/fonts/truetype/meiryo.ttc"
            font_size = 25
            font_pil = ImageFont.truetype(font_path, font_size)
            TextColor = (255, 255, 255)         # 白
            Text = "測定中"

            img_pil = Image.fromarray(result_frame)
            draw = ImageDraw.Draw(img_pil)
            positon = (10,280)
            draw.text(positon, Text, font = font_pil, fill = TextColor)
            img = np.array(img_pil)
            cv2.imshow('BodyTemperatureDetection_Text_Detect', img)

        if(state == "FINISH"):
            # カメラ画像とサーモグラフィー表示
            measure_start_time = time.time()
            #result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels)
            #result_frame = frame
            elapsed_time = time.time() - measure_start_time
            print ("1(Make_Camera_Tthermography):{0}".format(elapsed_time) + "[sec]")

            # カメラ画像を左右反転
            frame_flip_lr = cv2.flip(frame, 1)

            measure_start_time = time.time()
            # 最高温度表示
            MaxTempStr = str(Sensor.get_max_temperature()) + "℃"

            # 温度によって、表示するテキストの色を変える
            background_color = (0, 0, 0)
            if(Sensor.get_isfever() == True):
                #TextColor = (0, 0, 255)         # 赤
                TextColor = (255, 0, 0)         # 赤
                DetectResult = "正確な検温を行ってください。"
            else:
                TextColor = (0, 255, 0)         # 緑
                DetectResult = "平熱です。"

            #font_path = "/usr/share/fonts/truetype/meiryo.ttc"
            #font_size = 25
            #font_pil = ImageFont.truetype(font_path, font_size)
            #elapsed_time = time.time() - measure_start_time
            #print ("2:{0}".format(elapsed_time) + "[sec]")

            #measure_start_time = time.time()
            #img_pil = Image.fromarray(result_frame)
            #draw = ImageDraw.Draw(img_pil)
            #positon = (10,250)
            #draw.text(positon, MaxTempStr, font = font_pil, fill = TextColor)
            #img = np.array(img_pil)
            #elapsed_time = time.time() - measure_start_time
            #print ("3:{0}".format(elapsed_time) + "[sec]")

            # 測定結果表示
            #measure_start_time = time.time()
            #img_pil = Image.fromarray(img)
            #draw = ImageDraw.Draw(img_pil)
            #positon = (10,280)
            #draw.text(positon, DetectResult, font = font_pil, fill = TextColor)
            #img = np.array(img_pil)     
            #elapsed_time = time.time() - measure_start_time
            #print ("4:{0}".format(elapsed_time) + "[sec]")

            # OpenCVの画像をPygame用に変換
            pygame_image = convert_opencv_img_to_pygame(frame_flip_lr)

            # カメラ表示
            lcd.blit(pygame_image, (0, 0))

            # サーモ表示 ##########################################################################
            thermo_offset_x = 0
            thermo_offset_y = 480 - 160

            for ix, row in enumerate(bicubic):
                for jx, pixel in enumerate(row):
                    pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (thermo_offset_x + displayPixelHeight * ix, thermo_offset_y + displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
            # サーモ表示 ##########################################################################

            # 顔枠を表示
            pygame.draw.rect(lcd, (0, 0, 255), (220, 140, 200, 200), 3)

            # 文字表示(最高温度、測定結果) #############################
            pygame.font.init()

            font1 = pygame.font.SysFont("notosansmonocjkjp", 15, bold=True, italic=False)
            text1 = font1.render(MaxTempStr, True, TextColor, background_color)

            font2 = pygame.font.SysFont("notosansmonocjkjp", 15, bold=True, italic=False)
            text2 = font2.render(DetectResult, True, TextColor, background_color)

            lcd.blit(text1, (0,260))
            lcd.blit(text2, (0,290))
            # 文字表示 #############################

            # 描画していたSurfaceを拡大し、その描画先をdisplaySurfaceにする
            #pygame.transform.scale(lcd, (final_display_size_h, final_display_size_v), pygame.display.get_surface())

           # スプライトグループを更新
            group.update()

            # スプライトグループを描画
            group.draw(lcd)

            # 画面を更新
            pygame.display.update()

            for event in pygame.event.get():
                print("### event loop ###")
                print(event.type)

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_F2:
                    print("F2押下！！！！！")

                    # F2キーでフルスクリーンモードへの切り替え
                    fullscreen_flag = not fullscreen_flag
                    print("fullscreen_flag: " + str(fullscreen_flag))

                    if fullscreen_flag:
                        print("フルスクリーン")
                        lcd = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
                    else:
                        print("通常スクリーン")
                        lcd = pygame.display.set_mode(SCR_RECT.size)

            #measure_start_time = time.time()
            #cv2.imshow('BodyTemperatureDetection_Finish', img)
            #elapsed_time = time.time() - measure_start_time
            #print ("5(imshow):{0}".format(elapsed_time) + "[sec]")
        
        # キュー入力判定
        # "q"でループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # VideoCaptureオブジェクト破棄
    # USBカメラを閉じる
    cap.release()
    cv2.destroyAllWindows()


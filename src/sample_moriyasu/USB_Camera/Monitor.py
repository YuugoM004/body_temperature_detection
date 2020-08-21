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
import busio
import board

def Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels):

    # サーモグラフィー表示

    # bicubic補間したデータ
    measure_start_time = time.time()
    sensor_pixels_rotate = np.rot90(sensor_pixels, -1)
    fig = plt.imshow(sensor_pixels_rotate, cmap="inferno", interpolation="bicubic")
    elapsed_time = time.time() - measure_start_time
    print ("  imshow:{0}".format(elapsed_time) + "[sec]")

    # plt.colorbar()

    # plt.showだと止まってしまうので、pauseを使用
    # plt.clfしないとカラーバーが多数表示される
    measure_start_time = time.time()
    plt.pause(0.01)
    elapsed_time = time.time() - measure_start_time
    print ("  pause:{0}".format(elapsed_time) + "[sec]")

    measure_start_time = time.time()
    plt.clf()
    elapsed_time = time.time() - measure_start_time
    print ("  clf:{0}".format(elapsed_time) + "[sec]")

    # グレースケール表示
    measure_start_time = time.time()
    resize_width = 160
    resize_height = 160
    frame_resize = cv2.resize(frame,(resize_width, resize_height))
    elapsed_time = time.time() - measure_start_time
    print ("  resize:{0}".format(elapsed_time) + "[sec]")

    measure_start_time = time.time()
    frame_resized_gray = cv2.cvtColor(frame_resize,cv2.COLOR_BGR2GRAY)
    elapsed_time = time.time() - measure_start_time
    print ("  cvtColor:{0}".format(elapsed_time) + "[sec]")

    # グレースケール(2次元配列)をRGB(3次元配列)に変換する
    measure_start_time = time.time()
    frame_resized_gray_array = frame_resized_gray[:, :, None]

    height, width = frame_resized_gray.shape
    x_offset = 0
    y_offset = HEIGHT - resize_height

    frame[y_offset:height + y_offset, x_offset:width + x_offset] = frame_resized_gray_array
    elapsed_time = time.time() - measure_start_time
    print ("  other:{0}".format(elapsed_time) + "[sec]")

    return frame

def Monitor_Func(cap, WIDTH, HEIGHT, max_temp_fix, STATUS, DETECT_TH, sensor_pixels):

    print ("### Monitor_Func ###")
    print ("STATUS:" + STATUS)

    ## 本来はSensor.pyでやる処理だが、デバッグ用にここでセンサのインスタンスを取得
    # I2Cバスの初期化
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    # センサーの初期化
    sensor = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x68)
    # センサーの初期化待ち
    time.sleep(.1)
    ## ここまで

    plt.figure(figsize=(1, 1), dpi=160)

    while True:

        # カメラ画像取得
        # 1コマ分のキャプチャ画像データを読み込む
        _, frame = cap.read()
        if(frame is None):
            continue

        ## 本来はSensor.pyでやる処理だが、デバッグ用にここでセンサデータを取得
        # 8x8の表示
        # print (sensor.pixels)

        # 温度データ取得＆最高温度の計算
        measure_start_time = time.time()
        sensor_pixels = sensor.pixels
        max_temp = max(itertools.chain.from_iterable(sensor_pixels))
        print ("センサ最高温度:" + str(max_temp))
        elapsed_time = time.time() - measure_start_time
        print ("GetSensorData & CalcMaxTemp:{0}".format(elapsed_time) + "[sec]")
        ## ここまで


        if(STATUS == "WAIT"):
            print ("STATUS:" + STATUS)
        
            # カメラ画像とサーモグラフィー表示
            result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels)

            # 画像表示
            cv2.imshow('BodyTemperatureDetection', result_frame)


        if(STATUS == "DETECT"):
            print ("STATUS:" + STATUS)

            # カメラ画像とサーモグラフィー表示
            result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels)

            # 測定中を表示
            font_path = "/usr/share/fonts/truetype/meiryo.ttc"
            font_size = 40
            font_pil = ImageFont.truetype(font_path, font_size)
            TextColor = (255, 255, 255)         # 白
            Text = "測定中"

            img_pil = Image.fromarray(result_frame)
            draw = ImageDraw.Draw(img_pil)
            positon = (10,350)
            draw.text(positon, Text, font = font_pil, fill = TextColor)
            img = np.array(img_pil)
            cv2.imshow('BodyTemperatureDetection_Text_Detect', img)

        if(STATUS == "FINISH"):
            print ("STATUS:" + STATUS)

            # カメラ画像とサーモグラフィー表示
            measure_start_time = time.time()
            result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT, sensor_pixels)
            elapsed_time = time.time() - measure_start_time
            print ("1(Make_Camera_Tthermography):{0}".format(elapsed_time) + "[sec]")

            measure_start_time = time.time()
            # 最高温度表示
            MaxTempStr = str(max_temp) + "℃"

            # 温度によって、表示するテキストの色を変える
            if(max_temp >= DETECT_TH):
                TextColor = (0, 0, 255)         # 赤
                DetectResult = "正確な検温を行ってください。"
            else:
                TextColor = (0, 255, 0)         # 緑
                DetectResult = "平熱です。"

            font_path = "/usr/share/fonts/truetype/meiryo.ttc"
            font_size = 40
            font_pil = ImageFont.truetype(font_path, font_size)
            elapsed_time = time.time() - measure_start_time
            print ("2:{0}".format(elapsed_time) + "[sec]")

            measure_start_time = time.time()
            img_pil = Image.fromarray(result_frame)
            draw = ImageDraw.Draw(img_pil)
            positon = (10,300)
            draw.text(positon, MaxTempStr, font = font_pil, fill = TextColor)
            img = np.array(img_pil)
            elapsed_time = time.time() - measure_start_time
            print ("3:{0}".format(elapsed_time) + "[sec]")

            # 測定結果表示
            measure_start_time = time.time()
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            positon = (10,350)
            draw.text(positon, DetectResult, font = font_pil, fill = TextColor)
            img = np.array(img_pil)     
            elapsed_time = time.time() - measure_start_time
            print ("4:{0}".format(elapsed_time) + "[sec]")

            measure_start_time = time.time()
            cv2.imshow('BodyTemperatureDetection_Finish', img)
            elapsed_time = time.time() - measure_start_time
            print ("5(imshow):{0}".format(elapsed_time) + "[sec]")
        
        # キュー入力判定
        # "q"でループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # VideoCaptureオブジェクト破棄
    # USBカメラを閉じる
    cap.release()
    cv2.destroyAllWindows()


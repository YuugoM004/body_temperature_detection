# coding: utf-8

import time
import busio
import board

import itertools

#import cv2

# センサ接続に必要
import adafruit_amg88xx

import matplotlib.pyplot as plt

def Sensor_Func(DETECT_START_END_TH):

     print ("### Sensor_Func ###")

     # I2Cバスの初期化
     i2c_bus = busio.I2C(board.SCL, board.SDA) 

     # センサーの初期化
     sensor = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x68)

     # センサーの初期化待ち
     time.sleep(.1)

     # 8x8の表示
     print (sensor.pixels)
     sensor_pixels = sensor.pixels

     # センサから取得した8x8配列データが以下だとする
     # sensor.pixels =
     #sensor_pixels = [[27.25, 26.75, 26.75, 27.25, 27.75, 26.75, 27.75, 29.75],
     #                 [27.0,  27.25, 27.25, 26.75, 27.25, 27.5,  29.75, 32.5],
     #                 [27.25, 26.5,  26.75, 27.25, 27.0,  27.5,  27.75, 28.75],
     #                 [26.75, 25.5,  26.5,  23.5,  27.0,  36.8, 27.5,  33.5],
     #                 [26.75, 26.75, 26.75, 27.0,  27.25, 26.75, 27.25, 32.0],
     #                 [26.5,  26.5,  26.5,  27.25, 26.75, 27.0,  28.0,  32.25],
     #                 [26.5,  26.5,  26.5,  27.0,  27.0,  27.25, 28.0,  31.0],
     #                 [26.0,  26.5,  26.0,  26.5,  26.5,  26.75, 26.75, 27.75]]

     # 最高温度の計算
     max_temp = max(itertools.chain.from_iterable(sensor_pixels))
     print ("センサ最高温度:" + str(max_temp))

     # 8x8ピクセルの画像とbicubic補間をした画像を並べて表示させる
     #plt.subplots(figsize=(8, 4))

     # データ取得
     #sensordata = sensor_pixels

     # 8x8ピクセルのデータ
     #plt.subplot(1, 2, 1)
     #fig = plt.imshow(sensordata, cmap="inferno")
     #plt.colorbar()

     # bicubic補間したデータ
     #plt.subplot(1, 2, 2)
     #fig = plt.imshow(sensordata, cmap="inferno", interpolation="bicubic")
     #plt.colorbar()

     #plt.show()

     #############################################
     #MAX_TEMP = 36.7
     #STATUS = "WAIT"
     #STATUS = "DETECT"
     STATUS = "FINISH"

     # 8x8配列データ、最高温度、ステータスを返す
     return sensor_pixels, max_temp, STATUS 
     #############################################
# coding: utf-8

import os
import sys
import logging

import Camera
import Sensor

##################################################################
# 「初期化画面」を表示
def display_initialzie_screen_connect_checking():
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    logging.debug("start")

    print("「初期化画面」を表示")
    # 背景黒の画面を表示
    # メッセージ(しばらくお待ちください)を表示
    print("   [しばらくお待ちください]")

    logging.debug("end")

##################################################################
# 「初期化画面(接続確認の結果)」を表示
def display_initialzie_screen_connect_check_result(camera_connect_check_result, sensor_connect_check_result):
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    print("「初期化画面(接続確認の結果)」を表示")
    # 背景黒の画面を表示
    
    # 接続確認の結果を表示
    if(camera_connect_check_result):
        print("   [カメラの接続に成功しました]")
    else:
        print("   [カメラの接続に失敗しました]")

    if(sensor_connect_check_result):
        print("   [センサの接続に成功しました]")
    else:
        print("   [センサの接続に失敗しました]")

    if((camera_connect_check_result == False) or (sensor_connect_check_result == False)):
        print("   [電源OFFして、カメラとセンサの接続を確認後、再度電源ONしてください]")


##################################################################
# 「待機画面」「測定中画面」「測定終了画面」を表示
def display_wait_detect_finish_screen():
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    # [カメラ]映像取得
    Camera.get_capture()

    # [センサ]8x8配列の温度データを取得する
    Sensor.get_temperature_array()

    # [センサ]最高温度を取得する
    Sensor.get_max_temperature()

    # [センサ]状態を取得する
    Sensor.get_state()

    # [センサ]発熱であるかを取得する
    Sensor.get_isfever()

    # 状態によって表示する内容を切り替える
        # 待機画面を表示
            # カメラ画像を表示
            # サーモグラフィーを表示
        # 測定中画面を表示
            # カメラ画像を表示
            # サーモグラフィーを表示
            # メッセージ(測定中)を表示
        # 測定終了画面を表示ｄ
            # カメラ画像を表示
            # サーモグラフィーを表示
            # 測定温度を表示     
            # メッセージ(測定結果)を表示

##################################################################
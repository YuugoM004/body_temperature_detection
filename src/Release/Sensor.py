# coding: utf-8

import os
import sys
import logging
import time

from Adafruit_AMG88xx import Adafruit_AMG88xx

##################################################################
# 定数(iniファイルからの読み込み)
SENSOR_CONNECTED = 1
WAIT_TIME = 0
CORRECTION_VALUE = 0
DETECT_START_TEMPERATURE = 0
DETECT_START_FRAMENUM = 0
DETECT_CONTINUE_FRAMENUM = 0
FEVER_TEMPERATURE = 0

##################################################################
# モジュール変数
sensor = None  # センサのインスタンス
frame_counter = 0   # フレーム数カウンタ

# for Monitor
temperature_array = []    # 8x8の温度データ
max_temperature = 0   # FINISH状態で出力する最大温度
state = "WAIT" # 状態(WAIT:待機中/DETECT:計測中/FINISH:計測終了)
isfever = False     # 発熱有無(True:発熱あり/False:発熱なし)


##################################################################
def set_sensor_parameter(sensor_connected, wait_time, correction_value, detect_start_temperature, detect_start_framenum, detect_continue_framenum, fever_temperature):
    """センサで必要なパラメータを設定

    :param sensor_connected: センサ接続有無
    :param wait_time: センサ安定待ち時間
    :param correction_value: センサ補正値
    :param detect_start_temperature: 計測開始温度閾値
    :param detect_start_framenum: 計測開始温度閾値オーバー継続フレーム数
    :param detect_continue_framenum: 計測継続フレーム数
    :param fever_temperature: 発熱検知閾値
    """

    global SENSOR_CONNECTED
    SENSOR_CONNECTED = sensor_connected

    global WAIT_TIME
    WAIT_TIME = wait_time

    global CORRECTION_VALUE
    CORRECTION_VALUE = correction_value

    global DETECT_START_TEMPERATURE
    DETECT_START_TEMPERATURE = detect_start_temperature

    global DETECT_START_FRAMENUM
    DETECT_START_FRAMENUM = detect_start_framenum

    global DETECT_CONTINUE_FRAMENUM
    DETECT_CONTINUE_FRAMENUM = detect_continue_framenum

    global FEVER_TEMPERATURE
    FEVER_TEMPERATURE = fever_temperature


##################################################################
def sensor_connect_check():
    """センサの接続確認

    :return センサの接続結果(True:接続成功/False:接続失敗)
    """

    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    if SENSOR_CONNECTED == 1:
        # センサーの初期化
        global sensor
        sensor = Adafruit_AMG88xx()
        # センサーの初期化待ち
        time.sleep(.1)
        result = True

    else:
        result = True

    return result

##################################################################
def initialize_sensor():
    """センサの初期化

    :return センサの接続結果(True:接続成功/False:接続失敗)
    """

    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    logging.debug("start")

    # センサの接続確認
    result = sensor_connect_check()

    # センサ出力安定まで待機
    print(" センサ出力安定まで待機: {0} sec".format(WAIT_TIME))
    time.sleep(WAIT_TIME)

    logging.debug("end")

    return result

##################################################################
def measurement_temperature_and_status():
    """温度計測＆状態判定"""

    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    # 8x8配列の温度データを取得
    global temperature_array
    if SENSOR_CONNECTED == 1:
        temperature_array = sensor.readPixels()
    else:
        temperature_array = [27.25, 26.75, 26.75, 27.25, 27.75, 26.75, 27.75, 29.75, \
                            27.0,  27.25, 27.25, 26.75, 27.25, 27.5,  29.75, 32.5, \
                            27.25, 26.5,  26.75, 27.25, 27.0,  27.5,  27.75, 28.75, \
                            26.75, 25.5,  26.5,  23.5,  27.0,  34.75, 27.5,  33.5, \
                            26.75, 26.75, 26.75, 27.0,  27.25, 26.75, 27.25, 32.0, \
                            26.5,  26.5,  26.5,  27.25, 26.75, 27.0,  28.0,  32.25, \
                            26.5,  26.5,  26.5,  27.0,  27.0,  27.25, 28.0,  31.0, \
                            26.0,  26.5,  26.0,  26.5,  26.5,  26.75, 26.75, 27.75]

    print (temperature_array)

    # センサ出力値の補正
    # 30℃以上のところにゲタを履かせる
    temperature_array = list(map(lambda x: x + CORRECTION_VALUE if x >= 30.0 else x, temperature_array))

    # 最高温度を計算
    detect_max_temperature = max(temperature_array)
    print ("センサ最高温度:" + str(detect_max_temperature))

    # 状態を判定
    # WAIT->DETECT   : 最高温度が[DETECT_START_TEMPERATURE]を連続で[DETECT_START_FRAMENUM]フレーム超える
    # DETECT->FINISH : DETECT状態になってから最高温度が[DETECT_START_TEMPERATURE]を連続で[DETECT_CONTINUE_FRAMENUM]フレーム超える
    # DETECT->WAIT   : DETECT状態になってからFINISH条件になる前に最高温度が[DETECT_START_TEMPERATURE]以下になる
    # FINISH->WAIT   : 最高温度が[DETECT_START_TEMPERATURE]以下になる
    global state
    global isfever
    global max_temperature
    global frame_counter
    if state == "WAIT":
        if detect_max_temperature >= DETECT_START_TEMPERATURE:
            frame_counter = frame_counter + 1

            if frame_counter >= DETECT_START_FRAMENUM:
                frame_counter = 0
                state = "DETECT"    # WAIT->DETECT

        else:
            # 閾値以下になったらカウンタリセット
            frame_counter = 0

    elif state == "DETECT":
        if detect_max_temperature >= DETECT_START_TEMPERATURE:
            frame_counter = frame_counter + 1

            # 最高温度を保持
            if detect_max_temperature > max_temperature:
                max_temperature = detect_max_temperature

            if frame_counter >= DETECT_CONTINUE_FRAMENUM:
                # 発熱判定
                if max_temperature >= FEVER_TEMPERATURE:
                    isfever = True
                else:
                    isfever = False

                frame_counter = 0
                state = "FINISH"    # DETECT->FINISH

        else:
            # 閾値以下になったらWAIT状態に戻る
            max_temperature = 0
            frame_counter = 0
            state = "WAIT" # DETECT->WAIT

    elif state == "FINISH":
        if detect_max_temperature < DETECT_START_TEMPERATURE:
            max_temperature = 0
            isfever = False
            state = "WAIT" # FINISH->WAIT

    else:
        # 予期しない状態->諸々初期状態に戻してWAITにする
        frame_counter = 0
        max_temperature = 0
        isfever = False
        state = "WAIT"

    print ("state:" + state + str(frame_counter))


##################################################################
def get_temperature_array():
    """8x8配列の温度データを取得する

    :return temperature_array: 8x8配列の温度データ
    """

    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    return temperature_array

##################################################################
def get_max_temperature():
    """最高温度を取得する

    :return max_temperature: 最高温度
    """

    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    return max_temperature

##################################################################
def get_state():
    """状態を取得する

    :return state: 状態
    """

    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    return state

##################################################################
def get_isfever():
    """発熱有無を取得する

    :return isfever: 発熱有無
    """

    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    return isfever

##################################################################

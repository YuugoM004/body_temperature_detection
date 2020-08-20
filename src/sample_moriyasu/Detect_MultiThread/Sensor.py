# coding: utf-8

import os
import sys
import logging
import time

##################################################################
# カメラの接続確認
def sensor_connect_check():
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    result = True

    return result

##################################################################
# センサの初期化
def initialize_sensor(queued_request):
     print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

     logging.debug("start")

     # カメラの接続確認
     result = sensor_connect_check()

     # センサ出力安定まで待機
     print(" センサ出力安定まで待機")
     #time.sleep(15)
     time.sleep(2)

     #return result
     # キューに値を格納
     queued_request.put(result)

     logging.debug("end")

##################################################################
# 温度計測＆状態判定
def measurement_temperature_and_status():
     print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

     # 8x8配列の温度データを取得
     print(" 8x8配列の温度データを取得")
     # 最高温度を計算
     print(" 最高温度を計算")
     # 状態を判定
     print(" 状態を判定")
     # 発熱であるかを判定
     print(" 発熱であるかを判定")

##################################################################
# 8x8配列の温度データを取得する
def get_temperature_array():
     print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

##################################################################
# 最高温度を取得する
def get_max_temperature():
     print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

##################################################################
# 状態を取得する
def get_state():
     print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

##################################################################
# 発熱であるかを取得する
def get_isfever():
     print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

##################################################################


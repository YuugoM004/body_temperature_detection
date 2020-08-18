# coding: utf-8

import time

# 最高温度
MAX_TEMP_NUM = 0

def Sensor_Func(DETECT_START_END_TH):

     print ("### Sensor_Func ###")

     # 最高温度の計算
     
     # 計算結果
     MAX_TEMP_NUM = 36.8
     #STATUS = "WAIT"
     #STATUS = "DETECT"
     STATUS = "FINISH"

     # ステータスと温度を返す
     return STATUS, MAX_TEMP_NUM

     # 8x8の温度情報を返す
     #return array[]
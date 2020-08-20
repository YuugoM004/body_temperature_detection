# coding: utf-8

import os
import sys
import logging
import time
import threading
import queue

import Camera
import Sensor
import Monitor

############################################################################################################
def main():
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    # iniファイル読み込み
    print(" iniファイル読み込み")

    measure_start_time = time.time()
    #######################################################################################
    # カメラの初期化、センサの初期化、初期化画面を表示は並行処理(マルチスレッド)
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

    # キューを作成(キューはファーストインファーストアウト)
    queued_request = queue.Queue()

    # スレッドに関数を渡す
    # 初期化画面を表示
    thread1 = threading.Thread(target=Monitor.display_initialzie_screen_connect_checking)
    # カメラの初期化
    thread2 = threading.Thread(target=Camera.initialized_camera, args=(queued_request,))
    # センサの初期化
    thread3 = threading.Thread(target=Sensor.initialize_sensor, args=(queued_request,))

    # スレッドスタート
    print("### Thread Start ###")
    thread1.start()
    thread2.start()
    thread3.start()

    # スレッドから値を取得
    # カメラの初期化の方が先に終わるからとりあえずこれで大丈夫
    camera_connect_check_result = queued_request.get()
    sensor_connect_check_result = queued_request.get()
    #######################################################################################

    # 初期化画面(接続確認の結果)を表示
    Monitor.display_initialzie_screen_connect_check_result(camera_connect_check_result, sensor_connect_check_result)

    # 片方でも接続できていない場合は処理終了
    if((camera_connect_check_result == False) or (sensor_connect_check_result == False)):
        # 0:正常終了 1:異常終了
        sys.exit(1)
    
    # 経過時間計測
    elapsed_time = time.time() - measure_start_time
    print ("経過時間:{0}".format(elapsed_time) + "[sec]")

    # 初期化画面のスレッドの動作を確認するためにここで処理を終了する(本来は不要)
    #exit()


    LoopCnt = 0

    try:
        while True:
            print("################# LoopCnt:" + str(LoopCnt) + " #################")

            #####################################################################
            # モニタは、カメラ画像を自分で取得しにいく
            # モニタは、センサの「8x8配列の温度データ」「最高温度」「状態」「発熱であるか」の設定が終わるのを待つ必要がある
            # 上記の設定に時間がかかると表示が遅れそう
            # その場合はマルチスレッド化する
            
            # カメラ(カメラ画像はモニタからGet関数を呼んで取得するので、ここでやることは無い)

            # センサ(温度計測＆状態判定)
            Sensor.measurement_temperature_and_status()

            # モニタ(「待機画面」「測定中画面」「測定終了画面」を表示)
            Monitor.display_wait_detect_finish_screen()
            #####################################################################
            LoopCnt += 1

    # 終了処理
    # "Ctrl+C"でループから抜ける
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        # 0:正常終了 1:異常終了
        sys.exit(1)

############################################################################################################
if __name__ == '__main__':
    main()

print("### Program End ###")
############################################################################################################
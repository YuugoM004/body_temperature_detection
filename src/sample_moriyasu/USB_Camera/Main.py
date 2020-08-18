# coding: utf-8

import cv2
#print(cv2.__version__) 
import Camera
import Sensor
import Monitor

###################################################
# USBカメラ設定
# デバイスID
DEVICE_ID = 0
# ウインドウの幅
WIDTH = 800
# ウインドウの高さ
HEIGHT = 600
 # フレームレート
FPS = 24
###################################################
# ステータス(WAIT/DETECT/FINISH)
STATUS = "NONE"
# 測定開始の閾値
DETECT_START_END_TH = 35
# 測定結果の閾値
DETECT_TH = 37
###################################################

def main():
    # iniファイル読み込み


    # カメラ接続確認
    if(Camera.CameraConnectCheck(DEVICE_ID) == 1):
        STATUS = "WAIT"
    else:
    # メッセージを表示(メッセージボックスとか)
        print ("カメラの接続に失敗しました")
        exit()

    # センサ接続確認


    try:
        while True:
            # カメラ制御
            cap = Camera.Camera_Func(DEVICE_ID, WIDTH, HEIGHT, FPS)

            # センサ制御
            STATUS, MaxTemp = Sensor.Sensor_Func(DETECT_START_END_TH)
            print ("STATUS:" + STATUS)
            print ("最高温度:" + str(MaxTemp))

            # モニタ制御
            Monitor.Monitor_Func(cap, WIDTH, HEIGHT, MaxTemp, STATUS, DETECT_TH)

    # 終了処理
    # "Ctrl+C"でループから抜ける
    except KeyboardInterrupt:
        print ("KeyboardInterrupt")

        # VideoCaptureオブジェクト破棄
        # キャプチャデバイス(USBカメラ)を終了する
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

print ("### end ###")
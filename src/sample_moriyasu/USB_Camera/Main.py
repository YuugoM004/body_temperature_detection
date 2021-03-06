# coding: utf-8

import cv2
#print(cv2.__version__) 
import Camera
import Sensor
import Monitor_Pygame_blit_test

###################################################
# USBカメラ設定
# デバイスID
DEVICE_ID = 0
# ウインドウの幅
WIDTH = 640
# ウインドウの高さ
HEIGHT = 480
 # フレームレート
FPS = 10
###################################################
# ステータス(WAIT/DETECT/FINISH)
STATUS = "NONE"
# 測定開始の閾値
DETECT_START_END_TH = 35
# 測定結果の閾値
DETECT_TH = 37.5
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
            sensor_pixels, max_temp, STATUS = Sensor.Sensor_Func(DETECT_START_END_TH)
            print ("STATUS:" + STATUS)
            print ("最高温度:" + str(max_temp))

            # モニタ制御
            Monitor_Pygame_blit_test.Monitor_Func(cap, WIDTH, HEIGHT, max_temp, STATUS, DETECT_TH, sensor_pixels)

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

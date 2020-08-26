# coding: utf-8

import cv2
#print(cv2.__version__) 
import configparser

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
    ini = configparser.ConfigParser()

    try:
        ini.read('./config.ini')

        # カメラにiniファイルの内容を設定
        Camera.set_camera_parameter(int(ini['CAMERA']['DEVICE_ID']), \
                                    int(ini['CAMERA']['WIDTH']), \
                                    int(ini['CAMERA']['HEIGHT']), \
                                    int(ini['CAMERA']['FPS'])
                                    )

        # センサにiniファイルの内容を設定
        Sensor.set_sensor_parameter(int(ini['SENSOR']['SENSOR_CONNECTED']), \
                                    int(ini['SENSOR']['WAIT_TIME']), \
                                    int(ini['SENSOR']['DETECT_START_TEMPERATURE']), \
                                    int(ini['SENSOR']['DETECT_CONTINUE_FRAMENUM']), \
                                    int(ini['SENSOR']['FEVER_TEMPERATURE'])
                                    )

    except:
        print("iniファイルの読み込みに失敗しました。")


    # カメラ接続確認
    if(Camera.CameraConnectCheck() == 1):
        STATUS = "WAIT"
    else:
    # メッセージを表示(メッセージボックスとか)
        print ("カメラの接続に失敗しました")
        exit()

    # センサ初期化
    if Sensor.initialize_sensor() == False:
        print ("センサの接続に失敗しました")
        exit()


    try:
        while True:
            # カメラ制御
            cap = Camera.Camera_Func()

            # センサ制御
            #sensor_pixels, max_temp, STATUS = Sensor.Sensor_Func(DETECT_START_END_TH)
            #print ("STATUS:" + STATUS)
            #print ("最高温度:" + str(max_temp))

            # モニタ制御
            Monitor_Pygame_blit_test.Monitor_Func(cap, WIDTH, HEIGHT, 0, "WAIT", 0, [])

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

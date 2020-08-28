# coding: utf-8

import time
import pygame
import configparser

import Camera
import Sensor
import Monitor_Pygame_blit_test

#########################################################################################
def main():
    # iniファイル読み込み
    ini = configparser.ConfigParser()

    try:
        ini.read('./config.ini')
    except:
        print("iniファイルの読み込みに失敗しました。")

    # カメラにiniファイルの内容を設定
    Camera.set_camera_parameter(int(ini['CAMERA']['DEVICE_ID']), \
                                int(ini['CAMERA']['WIDTH']), \
                                int(ini['CAMERA']['HEIGHT']), \
                                int(ini['CAMERA']['FPS'])
                                )

    # センサにiniファイルの内容を設定
    Sensor.set_sensor_parameter(int(ini['SENSOR']['SENSOR_CONNECTED']), \
                                int(ini['SENSOR']['WAIT_TIME']), \
                                float(ini['SENSOR']['CORRECTION_VALUE']), \
                                float(ini['SENSOR']['DETECT_START_TEMPERATURE']), \
                                int(ini['SENSOR']['DETECT_START_FRAMENUM']), \
                                int(ini['SENSOR']['DETECT_CONTINUE_FRAMENUM']), \
                                float(ini['SENSOR']['FEVER_TEMPERATURE'])
                                )

    # モニタにiniファイルの内容を設定
    Monitor_Pygame_blit_test.set_monitor_parameter( \
                                int(ini['MONITOR']['CAMERA_WIDTH']), \
                                int(ini['MONITOR']['CAMERA_HEIGHT']), \
                                int(ini['MONITOR']['THERMO_WIDTH']), \
                                int(ini['MONITOR']['THERMO_HEIGHT']), \
                                float(ini['MONITOR']['THERMO_MINTEMP']), \
                                float(ini['MONITOR']['THERMO_MAXTEMP']), \
                                int(ini['MONITOR']['THERMO_COLORDEPTH'])
                                )

    # 初期化画面を表示
    Monitor_Pygame_blit_test.display_initialize_cheking()
    time.sleep(1)       # 表示がすぐ切り替わるので少し表示させておく

    # カメラ接続確認
    camera_connect_check_result = Camera.camera_connect_check()

    # センサ初期化(センサ接続確認)
    sensor_connect_check_result = Sensor.initialize_sensor()

    # 初期化画面(接続確認結果)を表示
    Monitor_Pygame_blit_test.display_initialize_checked(camera_connect_check_result, sensor_connect_check_result)
    time.sleep(2)           # 表示がすぐ切り替わるので少し表示させておく

    if((camera_connect_check_result == False) or (sensor_connect_check_result == False)):
        # 電源OFF画面を表示
        Monitor_Pygame_blit_test.display_turnoff()

    try:
        while True:
            # カメラ制御
            cap = Camera.get_camera_capture()

            # モニタ制御
            Monitor_Pygame_blit_test.display_wait_detect_finish(cap)

    # 終了処理
    # "Ctrl+C"でループから抜ける
    except KeyboardInterrupt:
        print ("KeyboardInterrupt")

        # VideoCaptureオブジェクト破棄
        # キャプチャデバイス(USBカメラ)を終了する
        cap.release()

        # Pygameの終了(画面閉じる)
        pygame.quit()

#########################################################################################
if __name__ == '__main__':
    main()

print ("### end ###")

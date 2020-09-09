# coding: utf-8

import time
import configparser

import pygame

import camera
import sensor
import monitor


def main():
    # iniファイル読み込み
    ini = configparser.ConfigParser()
    ini.read('./config.ini')

    try:
        # カメラにiniファイルの内容を設定
        camera.set_camera_parameter(int(ini['CAMERA']['DEVICE_ID']),
                                    int(ini['CAMERA']['WIDTH']),
                                    int(ini['CAMERA']['HEIGHT']),
                                    int(ini['CAMERA']['FPS'])
                                    )

        # センサにiniファイルの内容を設定
        sensor.set_sensor_parameter(int(ini['SENSOR']['SENSOR_CONNECTED']),
                                    int(ini['SENSOR']['WAIT_TIME']),
                                    float(ini['SENSOR']['CORRECTION_VALUE']),
                                    float(ini['SENSOR']['DETECT_START_TEMPERATURE']),
                                    int(ini['SENSOR']['DETECT_START_FRAMENUM']),
                                    int(ini['SENSOR']['DETECT_CONTINUE_FRAMENUM']),
                                    float(ini['SENSOR']['FEVER_TEMPERATURE'])
                                    )

        # モニタにiniファイルの内容を設定
        monitor.set_monitor_parameter(int(ini['MONITOR']['CAMERA_WIDTH']),
                                      int(ini['MONITOR']['CAMERA_HEIGHT']),
                                      int(ini['MONITOR']['THERMO_WIDTH']),
                                      int(ini['MONITOR']['THERMO_HEIGHT']),
                                      float(ini['MONITOR']['THERMO_MINTEMP']),
                                      float(ini['MONITOR']['THERMO_MAXTEMP']),
                                      int(ini['MONITOR']['THERMO_COLORDEPTH'])
                                      )
    except KeyError:
        # ConfigParser.read()ではiniファイルが読み込めなかった場合でも例外が発生しない
        # その後参照の段階でKeyErrorが発生するためここで捕捉する
        print("iniファイルが不正です")

    # 初期化画面を表示
    monitor.display_initialize_cheking()
    time.sleep(2)       # 表示がすぐ切り替わるので少し表示させておく

    # カメラ接続確認
    camera_connect_check_result = camera.camera_connect_check()

    # センサ初期化(センサ接続確認)
    sensor_connect_check_result = sensor.initialize_sensor()

    # 初期化画面(接続確認結果)を表示
    monitor.display_initialize_checked(camera_connect_check_result, sensor_connect_check_result)
    time.sleep(2)           # 表示がすぐ切り替わるので少し表示させておく

    if((camera_connect_check_result == False) or (sensor_connect_check_result == False)):
        # 電源OFF画面を表示
        monitor.display_turnoff()

    try:
        while True:
            # カメラ制御
            cap = camera.get_camera_capture()

            # モニタ制御
            monitor.display_wait_detect_finish(cap)

    # 終了処理
    # "Ctrl+C"でループから抜ける
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

        # VideoCaptureオブジェクト破棄
        # キャプチャデバイス(USBカメラ)を終了する
        cap.release()

        # Pygameの終了(画面閉じる)
        pygame.quit()


if __name__ == '__main__':
    main()

print("### end ###")

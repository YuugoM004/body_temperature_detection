# coding: utf-8

import os
import sys
import logging

##################################################################
# カメラの接続確認
def camera_connect_check():
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    result = True

    return result

##################################################################
# カメラの初期化
def initialized_camera(queued_request):
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

    logging.debug("start")

    #  カメラの接続確認
    result = camera_connect_check()

    # return result
    # キューに値を格納
    queued_request.put(result)

    logging.debug("end")

##################################################################
# カメラの映像取得
def get_capture():
    print("[" + os.path.basename(__file__) + "]" + sys._getframe().f_code.co_name)

##################################################################
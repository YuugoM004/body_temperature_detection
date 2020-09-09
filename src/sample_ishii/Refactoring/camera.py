# coding: utf-8

import cv2

##################################################################
# デフォルト(iniファイルからの読み込みで上書き)
# デバイスID
DEVICE_ID = 0
# ウインドウの幅
WIDTH = 640
# ウインドウの高さ
HEIGHT = 480
# フレームレート
FPS = 10


def set_camera_parameter(device_id, width, height, fps):
    """iniから読み込んだ値をカメラパラメータにセット

    :return なし
    """

    global DEVICE_ID
    DEVICE_ID = device_id

    global WIDTH
    WIDTH = width

    global HEIGHT
    HEIGHT = height

    global FPS
    FPS = fps


def camera_connect_check():
    """カメラの接続確認

    :return カメラの接続結果(True:接続成功/False:接続失敗)
    """

    # デバイスのオープン
    cap = cv2.VideoCapture(DEVICE_ID)

    if(cap.isOpened()):
        # 読み込み成功
        print("カメラ読み込み成功")
        return True
    else:
        # 読み込み失敗
        print("カメラ読み込み失敗")
        return False


def get_camera_capture():
    """カメラ画像のキャプチャ

    :return カメラで取得した画像(cv2.VideoCapture)
    """

    cap = cv2.VideoCapture(DEVICE_ID)

    # フォーマット・解像度・FPSの設定
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    return cap

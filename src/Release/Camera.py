# coding: utf-8

import cv2
#print(cv2.__version__) 

def CameraConnectCheck(DEVICE_ID):
    print ("### CameraConnectCheck ###")

    # デバイスのオープン
    cap = cv2.VideoCapture(DEVICE_ID)

    if(cap.isOpened()):
        #読み込み成功
        print ("カメラ読み込み成功")
        return 1
    else:
        #読み込み失敗
        print ("カメラ読み込み失敗")
        return 0

#########################################################################################
def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

#########################################################################################
def Camera_Func(DEVICE_ID, WIDTH, HEIGHT, FPS):

    print ("### Camera_Func ###")

    cap = cv2.VideoCapture(DEVICE_ID)

    # フォーマット・解像度・FPSの設定
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    # フォーマット・解像度・FPSの取得
    fourcc = decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print ("fourcc:{} fps:{} width:{} height:{}" .format(fourcc, fps, width, height))

    return cap
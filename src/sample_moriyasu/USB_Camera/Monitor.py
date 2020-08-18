# coding: utf-8

import cv2
print(cv2.__version__)
from PIL import ImageFont, ImageDraw, Image
import numpy as np

def Make_Camera_Tthermography(frame, WIDTH, HEIGHT):

    # サーモグラフィー表示

    # グレースケール表示
    resize_width = 200
    resize_height = 200
    frame_resize = cv2.resize(frame,(resize_width, resize_height))
    frame_resized_gray = cv2.cvtColor(frame_resize,cv2.COLOR_BGR2GRAY)

    # グレースケール(2次元配列)をRGB(3次元配列)に変換する
    frame_resized_gray_array = frame_resized_gray[:, :, None]

    height, width = frame_resized_gray.shape
    x_offset = 0
    y_offset = HEIGHT - resize_height

    frame[y_offset:height + y_offset, x_offset:width + x_offset] = frame_resized_gray_array

    return frame

def Monitor_Func(cap, WIDTH, HEIGHT, MaxTemp, STATUS, DETECT_TH):

    print ("### Monitor_Func ###")
    print ("STATUS:" + STATUS)

    while True:

        # カメラ画像取得
        # 1コマ分のキャプチャ画像データを読み込む
        _, frame = cap.read()
        if(frame is None):
            continue


        if(STATUS == "WAIT"):
            print ("STATUS:" + STATUS)
        
            # カメラ画像とサーモグラフィー表示
            result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT)

            # 画像表示
            cv2.imshow('BodyTemperatureDetection', result_frame)


        if(STATUS == "DETECT"):
            print ("STATUS:" + STATUS)

            # カメラ画像とサーモグラフィー表示
            result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT)

            # 測定中を表示
            font_path = "/usr/share/fonts/truetype/meiryo.ttc"
            font_size = 40
            font_pil = ImageFont.truetype(font_path, font_size)
            TextColor = (255, 255, 255)         # 白
            Text = "測定中"

            img_pil = Image.fromarray(result_frame)
            draw = ImageDraw.Draw(img_pil)
            positon = (10,350)
            draw.text(positon, Text, font = font_pil, fill = TextColor)
            img = np.array(img_pil)
            cv2.imshow('BodyTemperatureDetection_Text_Detect', img)

        if(STATUS == "FINISH"):
            print ("STATUS:" + STATUS)

            # カメラ画像とサーモグラフィー表示
            result_frame = Make_Camera_Tthermography(frame, WIDTH, HEIGHT)

            # 最高温度表示
            MaxTempStr = str(MaxTemp) + "℃"

            # 温度によって、表示するテキストの色を変える
            if(MaxTemp >= DETECT_TH):
                TextColor = (0, 0, 255)         # 赤
                DetectResult = "正確な検温を行ってください。"
            else:
                TextColor = (0, 255, 0)         # 緑
                DetectResult = "平熱です。"

            font_path = "/usr/share/fonts/truetype/meiryo.ttc"
            font_size = 40
            font_pil = ImageFont.truetype(font_path, font_size)

            img_pil = Image.fromarray(result_frame)
            draw = ImageDraw.Draw(img_pil)
            positon = (10,300)
            draw.text(positon, MaxTempStr, font = font_pil, fill = TextColor)
            img = np.array(img_pil)

            # 測定結果表示
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            positon = (10,350)
            draw.text(positon, DetectResult, font = font_pil, fill = TextColor)
            img = np.array(img_pil)     

            cv2.imshow('BodyTemperatureDetection_Finish', img)
        
        # キュー入力判定
        # "q"でループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # VideoCaptureオブジェクト破棄
    # USBカメラを閉じる
    cap.release()
    cv2.destroyAllWindows()


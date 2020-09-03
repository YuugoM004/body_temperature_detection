import cv2
import time

# デバイスID
DEVICE_ID = 0
# ウインドウの幅
WIDTH = 640
# ウインドウの高さ
HEIGHT = 480
 # フレームレート
FPS = 10

cap = cv2.VideoCapture(DEVICE_ID)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

# 顔検出ファイル
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

while True:
        # 時間計測
        time_start = time.time()

        # 画像取得、グレースケール変換
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 顔認識
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # print(len(faces))

        # 処理時間算出
        time_end = time.time()
        print(time_end - time_start)        

        # 円描画
        for (x,y,w,h) in faces:
            cv2.circle(img,(int(x+w/2),int(y+h/2)),int(w/2),(0, 0, 255),2) # red

        # 表示
        cv2.imshow('img',img)

        # 終了コマンド
        key = cv2.waitKey(10) 
        if key ==27 or key ==ord('q'): #escまたはqキーで終了
                break

cap.release()
cv2.destroyAllWindows()

print("Exit")   
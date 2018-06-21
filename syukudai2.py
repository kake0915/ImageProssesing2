import cv2
import numpy as np

def myfunc(i):
    pass

def craete_table(gamma):#1
    t = np.arange(256, dtype=np.uint8)
    for i in range(0, 255):
        j = 255 * (i / 255)**(1/gamma)
        if j < 0:
            t[i] = 0
        elif j > 255:
            t[i] = 255
        else:
            t[i] = j
    return t

cv2.namedWindow('title')# create win with win name
cv2.createTrackbar('value', 'title', 1,10, myfunc) # callback func

cap = cv2.VideoCapture(0)

while(True):

    ret,frame=cap.read()
    #カラーをグレーに変更
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #ガンマ補正（コントラスト）
    table = craete_table(gamma=1.5)#1
    gray = cv2.LUT(gray, table)#1
    #輪郭抽出
    lap = np.array([[1, 1,  1],[1, -8, 1],[1, 1,  1]])
    gray = cv2.filter2D(gray, -1,lap)#2
    #v*v平滑化フィルタでぼやかして輪郭を太くする
    v = cv2.getTrackbarPos('value','title')  # of the win
    v=v*2+1
    kernel = np.ones(shape=(v,v))
    kernel /=(v*v)
    gray = cv2.filter2D(gray, -1, kernel)
    #2値化
    _,gray =cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    #白黒反転
    gray = cv2.bitwise_not(gray)#3
    #ノイズ除去
    gray = cv2.medianBlur(gray,3)

    cv2.imshow('title',gray)

    if cv2.waitKey(1)== 27:
        break

cap.release()
cv2.destroyAllWindows()

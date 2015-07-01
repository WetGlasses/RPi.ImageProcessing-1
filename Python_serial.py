# RPi.ImageProcessing-2 with LED indicator
import numpy as np
import serial
import time
import cv2

def nothing(x):
    pass

windw = np.ones((4,4),np.uint8)

ser = serial.Serial("/dev/ttyUSB0" , baudrate=9600)


show = True

print('Which camera you want to use?')
C = input()
Cam = cv2.VideoCapture(C)
Cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
Cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

res, pic = Cam.read()
cv2.imshow('Control',pic)
cv2.createTrackbar('Low', 'Control', 0, 255, nothing)

while(1):
    res, uhu = Cam.read()
    B,G,R = cv2.split(uhu)
    if(show == True):
        low = cv2.getTrackbarPos('Low', 'Control')
    B= cv2.medianBlur(B,3)
    th, B= cv2.threshold(B, low, 255, cv2.THRESH_BINARY )
    B = cv2.morphologyEx(B, cv2.MORPH_OPEN , windw)
    B = cv2.morphologyEx(B, cv2.MORPH_CLOSE , windw)
    if(show == True):
        cv2.imshow('Control',B)
    cnt, h = cv2.findContours(B, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )
    if(len(cnt)>0):
        areaX=0
        pos=0
        for x in range (0, len(cnt)):
            area = cv2.contourArea(cnt[x])
            if(area>areaX):
                areaX=area
                pos=x
                
        cv2.drawContours(uhu, cnt,pos, (0,0,255),2)
        M=cv2.moments(cnt[pos])
        Cx= int(M['m10']/M['m00'])
        Cy= int(M['m01']/M['m00'])
        cv2.circle(uhu, (Cx, Cy), 5, (0,0,0), 2)
        CoOr = str(Cx)+' , '+str(Cy)
        cv2.putText (uhu, CoOr, (Cx,Cy),1,1, (0,255,0),)
    else:
        cv2.putText (uhu, 'Cannot find the object', (60,120), 1,1, (0,255,0))

    cv2.imshow('Tracking',uhu)
    if(show == False):
        if (Cx<140):
            ser.write('B')
        elif (Cx>180):
            ser.write('C')
        else:
            ser.write('A')
    k = cv2.waitKey(5)
    if(k==27):
        break
    elif(k==32):
        show = False

Cam.release()
cv2.destroyAllWindows()

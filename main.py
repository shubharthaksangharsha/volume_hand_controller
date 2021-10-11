import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
import alsaaudio
import pulsectl
wCam, hCam = 640, 480
ptime = 0 #previous time
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

# #getting volume controls 
# p = 0
# call(["amixer", "-D", "pulse", "sset", "Master", str(p)+"%"])
#volume controller 

m = alsaaudio.Mixer()
vol = 0
volBar = 400
volPerc = 0
detector = htm.handDetector(detectionConfidence=0.7)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lm = detector.findPosition(img, draw  = False)
    if len(lm) != 0:
        # print(lm[2], lm[8])
        #creating 2 circles
        x1,y1 = lm[4][1], lm[4][2]
        x2,y2 = lm[8][1], lm[8][2]
        cx, cy = (x1 + x2) // 2, (y1+ y2) //2
        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        #creating line between them 
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        #creating circle at midpoint of two fingers
        cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

        #calculating length 
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)
        #creating button at center
        if length < 50:
            cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)
        #hand range = 20 - 300
        #volume range = 0 - 100
        vol = np.interp(length,[50, 200], [0, 100])
        volBar = np.interp(length,[50, 200], [400, 150])
        volPerc = np.interp(length,[50, 200], [0, 100])


        print(int(length), int(vol))
        m.setvolume(int(vol))
    cv2.rectangle(img, (50,150), (84,400), (0, 255, 0), 3)
    cv2.rectangle(img, (50,int(volBar)), (84,400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(str(int(volPerc))) + "%", (40,450), cv2.FONT_HERSHEY_COMPLEX, 1,  (250,0,0), 3)

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img, str('FPS: ' + str(int(fps))), (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0 ,0), 3)
    cv2.imshow("Shubharthak-Volume-Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#!/usr/bin/python3

import cv2

def returnCameraindices():
    index = 0
    arr = []
    i = 10
    while i > 0:
        try:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
        except:
            pass
        index += 1
        i -= 1
    return arr

cameras = returnCameraindices()
#cameras=cameras[:2]
cap = {}

for c in cameras:
    cap[c] = cv2.VideoCapture(c)
    cap[c].set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap[c].set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    while True:
        ret,frame = cap[c].read()
        cv2.imshow('preview',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap[c].release()
    cv2.destroyAllWindows()
'''
cap = cv2.VideoCapture()
if not (cap.isOpened()):
    print("could not open video device")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
while(True):
    ret,frame = cap.read()
    cv2.imshow('preview', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

'''

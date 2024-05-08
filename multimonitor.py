#!/usr/bin/env python3

import cv2
import numpy as np
from numpy import sqrt
from datetime import datetime as dt
import time

rec_arr_size = 1000
cam_w = 640
cam_h = 480
thresh=400

def camera_indices(del_infrared=True):
    index = 0
    arr = []
    i = 10
    while i > 0:
        try:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                ret, frame = cap.read()
                if del_infrared:
                    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    h,s,v = cv2.split(hsvframe)
                    if np.max(s)>0:
                        arr.append(index)
                else:
                    arr.append(index)
                cap.release()
        except:
            pass
        index += 1
        i -= 1
    return arr


def get_grid_size(n):
    root = sqrt(n)
    divisors = []
    for curr_div in range(1,n):
        if n % float(curr_div + 1) == 0:
            divisors.append(curr_div + 1)
    h = min(range(len(divisors)), key=lambda i: abs(divisors[i]-sqrt(n)))
    if divisors[h]**2 == n:
        return divisors[h], divisors[h]
    else:
        w = h + 1
        return divisors[h], divisors[w]
        
def img_processor(img):
    gr_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(src=gr_img, ksize=(5,5), sigmaX=0)
    return blur_img

def get_contour_detections(mask, thresh=thresh):
    contours, _ = cv2.findContours(mask,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_TC89_L1)
    detections = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        area=w*h
        if area > thresh:
            detections.append([x,y,x+w,y+h,area])
    return np.array(detections)
    
cameras = camera_indices()
n_cams = len(cameras)

cap = []
for c in range(len(cameras)):
    curr = cv2.VideoCapture(cameras[c])
    curr.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    curr.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    cap.append(curr)

kernel = np.ones((10,10))
prev_frames=[None for _ in range(len(cameras))]
recorded = np.zeros((rec_arr_size,cam_h,n_cams*cam_w,3), dtype=np.uint8)
i=0
while True:
    frames = [] 
    thresh_frames = []
    for c in range(len(cap)):
        ret, frame = cap[c].read()
        proc_frame = img_processor(frame)
        if prev_frames[c] is None:
            prev_frames[c] = proc_frame
        diff_frame = cv2.absdiff(src1=prev_frames[c], src2=proc_frame)
        dil_frame = cv2.dilate(diff_frame, kernel,1)
        thresh_frame = cv2.threshold(src=dil_frame, thresh=50,
                                     maxval=255, type=cv2.THRESH_BINARY)[1]
        detections = get_contour_detections(thresh_frame)
        contours,_ = cv2.findContours(image=thresh_frame,
                                      mode=cv2.RETR_EXTERNAL,
                                      method=cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image=frame,
                         contours=contours,
                         contourIdx=-1,
                         color=(0,255,0),
                         thickness=2,
                         lineType=cv2.LINE_AA)
        prev_frames[c] = proc_frame
        frames.append(frame)
        thresh_frames.append(thresh_frame)
    full_frame = np.hstack((i for i in frames))
    full_thresh = np.hstack((i for i in thresh_frames))
    if np.any(full_thresh):
        if i<rec_arr_size:
            recorded[i,:,:,:] = full_frame
            i+=1
        else:
            pass
    cv2.imshow(' ', full_frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        now = str(dt.now())
        out = cv2.VideoWriter('output_'+now+'.avi',
                              cv2.VideoWriter_fourcc('M','J','P','G'),
                              30, (cam_w*n_cams, cam_h))
        out.write(recorded)
        break
[i.release() for i in cap]
cv2.destroyAllWindows()
np.save('output_array_'+now,recorded)

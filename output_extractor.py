#!/usr/bin/env python3

import sys
import argparse
import cv2

import os
folder = 'test'
in_file = 'output_2024-04-18 00:00:00.084035.avi'
if not os.path.isdir(folder):
    os.mkdir(folder)

vidcap = cv2.VideoCapture(in_file)
count = 0
while True:
    success, image = vidcap.read()
    if not success:
        break
    cv2.imwrite(os.path.join(folder, "frame{:d}.jpg".format(count)), image)
    count += 1
print("{} images are extracted in {}.".format(count,folder))

'''
def extractImages(in_pth, out_pth):
    vidcap = cv2.VideoCapture(in_pth)
    success, image = vidcap.read()
    count=0
    success = True
    while success:
        success, image = vidcap.read()
        print('read a new frame: ', success)
        cv2.imwrite(out_pth+"/frame%d.jpg" % count, image)
        count += 1

if __name__=='__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--in_pth', help='path to video')
    a.add_argument('--out_pth', help='path to images')
    args = a.parse_args()
    print(args)
    extractImages(args.in_pth, args.out_pth)
'''

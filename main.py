import cv2
import numpy as np

import os
import glob

import dlib
from skimage import io

import argparse

frames = []

persons = {} #value is array
cars = {}

num_frames_to_keep_trace = 10
trackers = []
trackers_trace = [] # key is a tracker, value is a list of rects for last num_frames_to_keep_trace

yolo_rect_file = ""
video_src_file = ""
vidoe_out_file = ""

def readYOLO():
  runningDataIdx = 0
  f = open(yolo_rect_file) #yolo rectangles
  lines = f.readlines()
  for i in lines:
    if "frame:" in i:
      tmp = i.strip().split(":")
      runningDataIdx = int(tmp[1])
    else:
      if ',' and 'person' in i:
        if runningDataIdx not in persons:
          persons[runningDataIdx] = []
        persons[runningDataIdx].append(parsRect(i))
      else:
        if runningDataIdx not in cars:
          cars[runningDataIdx] = []
        cars[runningDataIdx].append(parsRect(i))

def parsRect(data):
  tmp = data.strip().split(",")
  name = tmp[0]
  prob = float(tmp[1])
  left = int(tmp[2])
  right = int(tmp[3])
  top = int(tmp[4])
  bot = int(tmp[5])
  return (name, prob, left, right, top, bot)

def rectIntersection(a, b):
  dx = min(a.right(), b.right()) - max(a.left(), b.left())
  dy = min(a.bottom(), b.bottom()) - max(a.top(), b.top())
  if (dx>=0) and (dy>=0):
    intersection = dx * dy
    return intersection * 1.0 / (a.right() - a.left()) * (a.bottom() - a.top()) 
  else:
    return 0

def updateTrackers(frame):
  for i in trackers:
    i.update(frame)
    p = i.get_position()# 17:28 found error tracker.get_position()
    l = int(p.left())
    t = int(p.top())
    r = int(p.right())
    p = int(p.bottom())
    cv2.rectangle(frame, (l, t), (r, p), (0,0,255), 2)

def destroyTrackers(): #todo:
  pass

def mergeTrackers(): #todo:
  pass

def alreadyTracked(yolo_rect):
  for trac in trackers:
    if rectIntersection(trac.get_position(), yolo_rect) > 0.5:
      return True
  return False

def run():
  runningFrameIdx = 0
  cap = cv2.VideoCapture(video_src_file)

  if (cap.isOpened()== False): 
    print("Error opening video stream or file")

  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))

  out = cv2.VideoWriter(video_out_file, cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), 20, (frame_width,frame_height))

  while(cap.isOpened()):
    ret, frame = cap.read()
    runningFrameIdx += 1
    if ret == True:
      # 'aeroplane', ' 0.33', ' 886', ' 1003', ' 331', ' 377']
      # left, right, top, bot
      # ['car', ' 0.48', ' 500', ' 642', ' 386', ' 452']
      updateTrackers(frame)

      if runningFrameIdx in persons:
        for i in persons[runningFrameIdx]:
          cv2.rectangle(frame, (i[2], i[4]), (i[3], i[5]), (255,0,0), 2)
          
      if runningFrameIdx in cars:
        for i in cars[runningFrameIdx]:
          cv2.rectangle(frame, (i[2], i[4]), (i[3], i[5]), (0,255,0), 2)

      #l,t,r,b
      if runningFrameIdx in cars:
        for i in cars[runningFrameIdx]:
          # print(i)
          yolo_rect = dlib.rectangle(i[2], i[4], i[3], i[5])
          if alreadyTracked(yolo_rect): #> 50 %
            pass
          else:
            tracker = dlib.correlation_tracker()
            tracker.start_track(frame, yolo_rect)
            trackers.append(tracker)

      #todo: add tracker for persons
        
      out.write(frame)

      #todo: remove
      # if runningFrameIdx > 100: 
      #   break

    else:
      break

  cap.release()
  out.release()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--src', help='video file', default='test.flv')
  parser.add_argument('--src_dat', help='YOLO rects for video', default='test.dat') #video preprocessed
  parser.add_argument('--dst', help='destination video file', default='test.avi')
  
  args = parser.parse_args()
  yolo_rect_file = args.src_dat
  video_src_file = args.src
  video_out_file = args.dst

  readYOLO()
  run()

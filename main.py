import cv2
import numpy as np

import os
import glob

import dlib
from skimage import io

frames = []

persons = {} #value is array
cars = {}

trackers = []

def readYOLO():
  runningDataIdx = 0
  f = open("test.dat") #yolo rectangles
  lines = f.readlines()
  for i in lines:
    if "frame:" in i:
      tmp = i.strip().split(":")
      runningDataIdx = int(tmp[1])
      # print(runningDataIdx)
    else:
      if ',' and 'person' in i:
        # print(parsRect(i))
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

# def destroyTrackers():
#   for i in trackers:
#     for j in trackers:
#       if i != j and rectIntersection(i.get_position(), j.get_position()) > 0.5:
#         trackers.remove(j)

def mergeTrackers():
  pass

def alreadyTracked(yolo_rect):
  for trac in trackers:
    if rectIntersection(trac.get_position(), yolo_rect) > 0.5:
      return True
  return False

def run():
  runningFrameIdx = 0
  cap = cv2.VideoCapture('test.flv')

  if (cap.isOpened()== False): 
    print("Error opening video stream or file")

  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))

  out = cv2.VideoWriter('res.avi',cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), 20, (frame_width,frame_height))

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

      # print('frame: {0}, trackers: {1}'.format(runningFrameIdx, len(trackers)))
        
      out.write(frame)

      # if runningFrameIdx > 300:
      #   break
    else:
      break

  cap.release()
  out.release()

if __name__ == "__main__":
  readYOLO()
  run()

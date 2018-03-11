import cv2
import numpy as np

def parsRect(data):
  tmp = data.strip().split(",")
  # print(tmp)
  name = tmp[0]
  prob = float(tmp[1])
  left = int(tmp[2])
  right = int(tmp[3])
  top = int(tmp[4])
  bot = int(tmp[5])
  return (name, prob, left, right, top, bot)

frames = []
f = open("test.dat")
runningDataIdx = 0

persons = {} #value is array
cars = {}

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



runningFrameIdx = 0

# print(persons[263])
# print(persons[263][2])



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
    # ['car', ' 0.48', ' 500', ' 642', ' 386', ' 452']
    # left, right, top, bot

    if runningFrameIdx in persons:
      for i in persons[runningFrameIdx]:
        cv2.rectangle(frame, (i[2], i[4]), (i[3], i[5]), (255,0,0), 2)
        
    if runningFrameIdx in cars:
      for i in cars[runningFrameIdx]:
        cv2.rectangle(frame, (i[2], i[4]), (i[3], i[5]), (0,255,0), 2)

    out.write(frame)
  else:
    break

cap.release()
out.release()

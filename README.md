# aihack (CRT problem solving...)

## Data

test.dat Пример аварии.flv

test2.dat Два торопыги.flv

## Idea behind

* Preprocess video by YOLO (phase 1)
https://github.com/hoopoe/darknet/commits/master

* Enable dlib correlation tracker to remove noisy rectangles (phase 2)
  
## Projects used
We used several projects, that helped us a lot of 
* dlib - for correlation tracker purpose
* YOLA - for fragmenting cars based on the frame
* darknet/+ that just persist file on the disk

## Algorithm description

![Algorithm description](hack-ai-crt-flow.png)

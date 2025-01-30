import numpy as np
import cv2 as cv
from vilib import Vilib



Vilib.camera_start()
Vilib.display()
edges = cv.Canny(img,100,200)

from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start(show_preview=True)
